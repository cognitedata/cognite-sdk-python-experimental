from typing import Dict, List

from cognite.experimental._context_client import ContextModelAPI
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel


class EntityMatchingAPI(ContextModelAPI):
    _RESOURCE_PATH = "/context/entity_matching"
    _MODEL_CLASS = EntityMatchingModel

    def fit(self, items: List[str]) -> "Task[EntityMatchingModel]":
        """Fit entity matching model.

        Args:
            items: list of entities to create a model for.

        Returns:
            Task[EntityMatchingModel]: Task which waits for the model to be completed."""
        return super()._fit_model(items=list(items))

    def create_rules(self, matches: List[Dict]) -> "Task[ContextualizationJob]":
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a dictionary of from: to matches.

        Returns:
            Task[ContextualizationJob]: Task which waits for the job to be completed."""
        return self._run_job(job_path="/rules", status_path="/rules/", items=matches)
