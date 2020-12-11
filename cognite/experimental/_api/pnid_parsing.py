from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI


class PNIDParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/pnid"

    def detect(
        self,
        entities: List[Union[str, dict]],
        search_field: str = "name",
        name_mapping: Dict[str, str] = None,
        partial_match: bool = False,
        min_tokens: int = 1,
        file_id: int = None,
        file_external_id: str = None,
    ) -> ContextualizationJob:
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
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        if not (
            all([isinstance(entity, str) for entity in entities])
            or all([isinstance(entity, dict) for entity in entities])
        ):
            raise ValueError("all the elements in entities must have same type (either str or dict)")

        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        entities, entities_return = self._detect_before_hook(entities, search_field)

        job = self._run_job(
            job_path="/detect",
            status_path="/detect/",
            file_id=file_id,
            file_external_id=file_external_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
        )
        job.wait_for_completion()
        if job.status == "Completed":
            job = self._detect_after_hook(job, entities_return, search_field)
        return job

    @staticmethod
    def _detect_before_hook(entities, search_field):
        """To decide whether to use search_field or not and make sure the entities are of type List[str]
        """
        entities_return = None
        if entities and isinstance(entities[0], dict):
            entities_return = entities.copy()
            entities = [entity.get(search_field) for entity in entities]
        return entities, entities_return

    @staticmethod
    def _detect_after_hook(job, entities_return, search_field):
        """Insert the entities into the result if search_field is used
        """
        if entities_return:
            texts = {item.get("text") for item in job.result["items"]}
            entities_return = [entity for entity in entities_return if entity.get(search_field) in texts]
            for item in job.result["items"]:
                item["entities"] = [entity for entity in entities_return if entity.get(search_field) == item["text"]]
        return job

    def extract_pattern(
        self, patterns: List[str], file_id: int = None, file_external_id: str = None
    ) -> ContextualizationJob:
        """Extract tags from P&ID based on pattern

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            patterns (list): List of regular expression patterns to look for in the P&ID. See API docs for details.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        if file_id is None and file_external_id is None:
            raise ValueError("File id and file external id cannot both be none")

        return self._run_job(
            job_path="/extractpattern",
            status_path="/extractpattern/",
            file_id=file_id,
            file_external_id=file_external_id,
            patterns=patterns,
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
        )
