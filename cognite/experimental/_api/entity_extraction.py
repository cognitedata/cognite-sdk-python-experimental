from typing import List

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import ContextualizationJob


class EntityExtractionAPI(ContextAPI):
    _RESOURCE_PATH = "/context/entity_extraction"

    def extract(self, file_ids: List[int], entities: List[str]) -> "Task[ContextualizationJob]":
        """Extracts entities from files.

        Args:
            file_ids: List of file ids to search.
            entities: Entities to search for.

        Returns:
            Task[ContextualizationJob]: Task which waits for the job to be completed."""
        return self._run_job(job_path="/extract", file_ids=file_ids, entities=entities)
