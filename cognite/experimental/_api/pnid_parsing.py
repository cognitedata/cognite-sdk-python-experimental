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

        if not (
            all([isinstance(entity, str) for entity in entities])
            or all([isinstance(entity, dict) for entity in entities])
            or all([isinstance(entity, CogniteResource) for entity in entities])
        ):
            raise ValueError("all the elements in entities must have same type (either str or dict)")

        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        entities, entities_field_to_objects = self._detect_before_hook(entities, search_field)

        job = self._run_job(
            job_path="/detect",
            status_path="/detect/",
            file_id=file_id,
            file_external_id=file_external_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
            job_cls=PNIDDetectResults,
        )
        job._set_entities_field_to_objects(entities_field_to_objects)
        return job

    @staticmethod
    def _detect_before_hook(entities, search_field):
        """To decide whether to use search_field or not and make sure the entities are of type List[str]"""
        if entities and isinstance(entities[0], CogniteResource):
            entities = [entity.dump(camel_case=True) for entity in entities]

        if entities and isinstance(entities[0], dict):
            entities_field_to_objects = defaultdict(list)
            converted_entities = [entity.get(search_field) for entity in entities]
            for entity_field, entity_obj in zip(converted_entities, entities):
                entities_field_to_objects[entity_field].append(entity_obj)
            return converted_entities, entities_field_to_objects
        else:
            return entities, None

    def extract_pattern(
        self, patterns: List[str], file_id: int = None, file_external_id: str = None
    ) -> PNIDDetectResults:
        """Extract tags from P&ID based on pattern

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
        """Convert a P&ID to an interactive SVG where the provided annotations are highlighted

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            items (List[Dict]): List of entity annotations for entities detected in the P&ID.
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
