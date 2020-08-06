from typing import Dict, List, Tuple, Union

from cognite.client.data_classes._base import CogniteResource
from cognite.experimental._context_client import ContextModelAPI
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel


class EntityMatchingAPI(ContextModelAPI):
    _RESOURCE_PATH = EntityMatchingModel._RESOURCE_PATH
    _MODEL_CLASS = EntityMatchingModel

    def fit(
        self,
        match_from: List[Union[Dict, CogniteResource]],
        match_to: List[Union[Dict, CogniteResource]],
        true_matches: List[Tuple[int, int]] = None,
        keys_from_to: List[Tuple[str, str]] = None,
        feature_type: str = None,
        classifier: str = None,
        complete_missing: bool = False,
    ) -> EntityMatchingModel:
        """Fit entity matching model with machine learning methods.

        Args:
            match_from: entities to match from, should have an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list)
            match_to: entities to match to, should have an 'id' field.  Tolerant to passing more than is needed or used.
            true_matches: Known valid matches given as a list of (id_from,id_to). If omitted, uses an unsupervised model.
            keys_from_to: List of (from,to) keys to use in matching. Default in the API is [('name','name')]
            feature_type (str): feature type that defines the combination of features used, see API docs for details.
            classifier (str): classifier used in training. Currently undocumented in API.
            complete_missing (bool): whether missing data in keyFrom or keyTo should return error or be filled in with an empty string. Currently undocumented in API
        Returns:
            EntityMatchingModel: Resulting queued model."""
        if keys_from_to:
            keys_from_to = [{"keyFrom": f, "keyTo": t} for f, t in keys_from_to]
        if true_matches:
            true_matches = list(true_matches)
        return super()._fit_model(
            model_path="/fit",
            match_from=EntityMatchingModel.dump_entities(match_from),
            match_to=EntityMatchingModel.dump_entities(match_to),
            true_matches=true_matches,
            keys_from_to=keys_from_to,
            feature_type=feature_type,
            classifier=classifier,
            complete_missing=complete_missing,
        )

    def fit_ml(
        self,
        match_from: List[Union[Dict, CogniteResource]],
        match_to: List[Union[Dict, CogniteResource]],
        true_matches: List[Tuple[int, int]] = None,
        keys_from_to: List[Tuple[str, str]] = None,
        feature_type: str = None,
        classifier: str = None,
        complete_missing: bool = False,
    ) -> EntityMatchingModel:
        """Duplicate of fit will eventually be removed"""
        if keys_from_to:
            keys_from_to = [{"keyFrom": f, "keyTo": t} for f, t in keys_from_to]
        if true_matches:
            true_matches = list(true_matches)
        return super()._fit_model(
            model_path="/fit",
            match_from=EntityMatchingModel.dump_entities(match_from),
            match_to=EntityMatchingModel.dump_entities(match_to),
            true_matches=true_matches,
            keys_from_to=keys_from_to,
            feature_type=feature_type,
            classifier=classifier,
            complete_missing=complete_missing,
        )

    def create_rules(self, matches: List[Dict]) -> ContextualizationJob:
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a list of dictionaries with 'input', 'predicted' and (optionally) 'score'

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/rules", items=matches)
