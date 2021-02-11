from collections import defaultdict
from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import CogniteResource

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import (
    PNIDConvertResults,
    PNIDDetectionList,
    PNIDDetectionPageList,
    PNIDDetectResults,
)


class PNIDParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/pnid"

    def detect(
        self,
        entities: List[Union[str, dict, CogniteResource]],
        search_field: str = "name",
        name_mapping: Dict[str, str] = None,
        partial_match: bool = False,
        min_tokens: int = 1,
        file_id: int = None,
        file_external_id: str = None,
    ) -> PNIDDetectResults:
        """Detect entities in a PNID.
        The results are not written to CDF.
        Note: All users on this CDF subscription with assets read-all and files read-all capabilities in the project,
        are able to access the data sent to this endpoint.

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            file_external_id: File external id
            entities (List[Union[str, dict]]): List of entities to detect
            search_field (str): If entities is a list of dictionaries, this is the key to the values to detect in the PnId
            name_mapping (Dict[str,str]): Optional mapping between entity names and their synonyms in the P&ID. Used if the P&ID contains names on a different form than the entity list (e.g a substring only). The response will contain names as given in the entity list.
            partial_match (bool): Allow for a partial match (e.g. missing prefix).
            min_tokens (int): Minimal number of tokens a match must be based on
        Returns:
            PNIDDetectResults: Resulting queued job. Note that .results property of this job will block waiting for results."""

        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        entities = [
            entity.dump(camel_case=True) if isinstance(entity, CogniteResource) else entity for entity in entities
        ]

        job = self._run_job(
            job_path="/detect",
            status_path="/detect/",
            file_id=file_id,
            file_external_id=file_external_id,
            entities=entities,
            partial_match=partial_match,
            search_field=search_field,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
            job_cls=PNIDDetectResults,
        )
        return job

    def extract_pattern(
        self, patterns: List[str], file_id: int = None, file_external_id: str = None
    ) -> PNIDDetectResults:
        """Extract tags from P&ID based on pattern. The results are not written to CDF.

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            patterns (list): List of regular expression patterns to look for in the P&ID. See API docs for details.

        Returns:
            PNIDDetectResults: Resulting queued job. Note that .results property of this job will block waiting for results."""

        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        return self._run_job(
            job_path="/extractpattern",
            status_path="/extractpattern/",
            file_id=file_id,
            file_external_id=file_external_id,
            patterns=patterns,
            job_cls=PNIDDetectResults,
        )

    def convert(
        self, items: List[Dict], grayscale: bool = None, file_id: int = None, file_external_id: str = None
    ) -> ContextualizationJob:
        """Convert a P&ID to an interactive SVG where the provided annotations are highlighted.
        The resulting SVG is not uploaded to CDF.

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            items (List[Dict]): List of entity annotations for entities detected in the P&ID.
                For instance the resulting items from calling the detect or extract_pattern-method.
            grayscale (bool, optional): Return the SVG version in grayscale colors only (reduces the file size). Defaults to None.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results.
        """
        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        return self._run_job(
            job_path="/convert",
            status_path="/convert/",
            file_id=file_id,
            file_external_id=file_external_id,
            items=items,
            grayscale=grayscale,
            job_cls=PNIDConvertResults,
        )

    def ocr(self, file_id: int,) -> PNIDDetectionPageList:
        """Retrieve the cached raw OCR result. Only works when detect (or the vision ocr service) has already been used on the file.

        Args:
            file_id (int): ID of the file.

        Returns:
            PNIDDetectionPageList  (effectively List[PNIDDetectionList]): Cached OCR results, one list per page."""
        res = self._post(f"{self._RESOURCE_PATH}/ocr", json={"fileId": file_id})
        items = [
            PNIDDetectionList._load(item["annotations"], cognite_client=self._cognite_client)
            for item in res.json()["items"]
        ]
        return PNIDDetectionPageList(items, file_id=file_id)
