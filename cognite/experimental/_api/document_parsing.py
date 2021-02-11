from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import CogniteResource

from cognite.experimental._context_client import ContextAPI


class DocumentParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/documents"

    def detect(
        self,
        file_id: int,
        entities: List[Union[str, dict, CogniteResource]],
        name_mapping: Dict[str, str] = None,
        partial_match: bool = False,
        min_tokens: int = 1,
        search_field: str = "name",
    ) -> ContextualizationJob:
        """Detect entities in a document

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            entities (List[Union[str, dict, CogniteResource]]): List of entities to detect
            name_mapping (Dict[str,str]): Optional mapping between entity names and their synonyms in the document. Used if the document contains names on a different form than the entity list (e.g a substring only). The response will contain names as given in the entity list.
            partial_match (bool): Allow for a partial match (e.g. missing prefix).
            min_tokens (int): Minimal number of tokens a match must be based on
            search_field (str): Name of the field of non-string entities that identify them.
        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        entities = [
            entity.dump(camel_case=True) if isinstance(entity, CogniteResource) else entity for entity in entities
        ]

        return self._run_job(
            job_path="/detect",
            status_path="/",
            file_id=file_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
            min_tokens=min_tokens,
            search_field=search_field,
        )
