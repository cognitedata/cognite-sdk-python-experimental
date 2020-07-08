from typing import Dict, List

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import ContextualizationJob


class SchemaCompletionAPI(ContextAPI):
    _RESOURCE_PATH = "/schemas"

    def complete(self, external_id: str) -> ContextualizationJob:
        """Completes a schema uploaded in CDF as a type.

        Args:
            external_id (str): External ID of the type to be completed

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/complete", status_path="/", external_id=external_id,)
