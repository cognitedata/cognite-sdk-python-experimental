from typing import Dict, List, Union

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import ContextualizationJob


class PNIDParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/pnid"

    def detect(
        self,
        file_id: int,
        entities: List[Union[str, dict]],
        search_field: str = "name",
        name_mapping: Dict[str, str] = None,
        partial_match: bool = False,
        min_tokens: int = 1,
    ) -> ContextualizationJob:
        """Detect entities in a PNID

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            entities (List[Union[str, dict]]): List of entities to detect
            name_mapping (Dict[str,str]): Optional mapping between entity names and their synonyms in the P&ID. Used if the P&ID contains names on a different form than the entity list (e.g a substring only). The response will contain names as given in the entity list.
            partial_match (bool): Allow for a partial match (e.g. missing prefix).
            min_tokens (int): Minimal number of tokens a match must be based on
        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        if entities and isinstance(entities[0], dict):
            entities = [entity.get(search_field) for entity in entities]

        return self._run_job(
            job_path="/detect",
            status_path="/detect/",
            file_id=file_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
        )

    def extract_pattern(self, file_id, patterns: List[str]) -> ContextualizationJob:
        """Extract tags from P&ID based on pattern

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            patterns (list): List of regular expression patterns to look for in the P&ID. See API docs for details.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(
            job_path="/extractpattern", status_path="/extractpattern/", file_id=file_id, patterns=patterns,
        )

    def convert(self, file_id: int, items: List[Dict], grayscale: bool = None,) -> ContextualizationJob:
        """Convert a P&ID to an interactive SVG where the provided annotations are highlighted

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            items (List[Dict]): List of entity annotations for entities detected in the P&ID.
            grayscale (bool, optional): Return the SVG version in grayscale colors only (reduces the file size). Defaults to None.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results.
        """
        return self._run_job(
            job_path="/convert", status_path="/convert/", file_id=file_id, items=items, grayscale=grayscale,
        )
