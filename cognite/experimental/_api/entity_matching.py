from typing import Dict, List

from cognite.experimental._context_client import ContextModelAPI
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel


class EntityMatchingAPI(ContextModelAPI):
    _RESOURCE_PATH = EntityMatchingModel._RESOURCE_PATH
    _MODEL_CLASS = EntityMatchingModel

    def fit(self, items: List[str]) -> EntityMatchingModel:
        """Fit entity matching model.

        Args:
            items: list of entities to create a model for.

        Returns:
            EntityMatchingModel: Resulting queued model."""
        return super()._fit_model(items=list(items))

    def create_rules(self, matches: List[Dict]) -> ContextualizationJob:
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a dictionary of from: to matches.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/rules", items=matches)
