from typing import Dict, List

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import ContextualizationJob


class DocumentParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/documents"

    def detect(
        self,
        file_id: int,
        entities: List[str],
        name_mapping: Dict[str, str] = None,
        partial_match: bool = False,
        min_tokens: int = 1,
    ) -> ContextualizationJob:
        """Detect entities in a document

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            entities (List[str]): List of entities to detect
            name_mapping (Dict[str,str]): Optional mapping between entity names and their synonyms in the document. Used if the document contains names on a different form than the entity list (e.g a substring only). The response will contain names as given in the entity list.
            partial_match (bool): Allow for a partial match (e.g. missing prefix).
            min_tokens (int): Minimal number of tokens a match must be based on
        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(
            job_path="/detect",
            status_path="/",
            file_id=file_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
        )
