from typing import List

from cognite.experimental._context_client import ContextAPI


class EntityExtractionAPI(ContextAPI):
    _RESOURCE_PATH = "/context/entity_extraction"

    def extract(self, file_ids: List[int], entities: List[str]) -> "ContextualizationJob":
        """Extracts entities from files.

        Args:
            file_ids: List of file ids to search.
            entities: Entities to search for.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/extract", status_path="/", file_ids=file_ids, entities=entities)
