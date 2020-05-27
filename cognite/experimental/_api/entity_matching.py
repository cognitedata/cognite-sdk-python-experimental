from typing import Dict, List, Tuple, Union

from cognite.client.data_classes._base import CogniteResource
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

    def fit_ml(
        self,
        match_from: List[Union[Dict, CogniteResource]],
        match_to: List[Union[Dict, CogniteResource]],
        true_matches: List[Tuple[int, int]] = None,
        keys_from_to: List[Tuple[str, str]] = None,
        model_type=None,
    ) -> EntityMatchingModel:
        """Fit entity matching model with machine learning methods.

        Args:
            match_from: entities to match from, should have an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list)
            match_to: entities to match to, should have an 'id' field.  Tolerant to passing more than is needed or used.
            true_matches: Known valid matches given as a list of (id_from,id_to). If ommited, uses an unsupervised model.
            keys_from_to: List of (from,to) keys to use in matching. Default in the API is [('name','name')]
            model_type: model type that defines features and methods used, see API docs for details.

        Returns:
            EntityMatchingModel: Resulting queued model."""
        if keys_from_to:
            keys_from_to = [{"keyFrom": f, "keyTo": t} for f, t in keys_from_to]
        if true_matches:
            true_matches = list(true_matches)
        return super()._fit_model(
            model_path="/fitml",
            match_from=EntityMatchingModel.dump_entities(match_from),
            match_to=EntityMatchingModel.dump_entities(match_to),
            true_matches=true_matches,
            keys_from_to=keys_from_to,
            model_type=model_type,
        )

    def create_rules(self, matches: List[Dict]) -> ContextualizationJob:
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a list of dictionaries with 'input', 'predicted' and (optionally) 'score'

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/rules", items=matches)
