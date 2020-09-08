from typing import Dict, List, Optional, Tuple, Union

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource
from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import (
    ContextualizationJob,
    EntityMatchingModel,
    EntityMatchingModelList,
    EntityMatchingModelUpdate,
)


class EntityMatchingAPI(ContextAPI):
    _RESOURCE_PATH = EntityMatchingModel._RESOURCE_PATH
    _LIST_CLASS = EntityMatchingModelList

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[EntityMatchingModel]:
        """Retrieve model

        Args:
            id: id of the model to retrieve.
            external_id: external id of the model to retrieve.

        Returns:
            EntityMatchingModel: Model requested."""
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def retrieve_multiple(
        self, ids: Optional[List[int]] = None, external_ids: Optional[List[str]] = None
    ) -> EntityMatchingModelList:
        """Retrieve models

        Args:
            ids: ids of the model to retrieve.
            external_ids: external ids of the model to retrieve.

        Returns:
            EntityMatchingModelList: Models requested."""
        utils._auxiliary.assert_type(ids, "id", [List], allow_none=True)
        utils._auxiliary.assert_type(external_ids, "external_id", [List], allow_none=True)
        return self._retrieve_multiple(ids=ids, external_ids=external_ids, wrap_ids=True)

    def update(
        self,
        item: Union[
            EntityMatchingModel, EntityMatchingModelUpdate, List[Union[EntityMatchingModel, EntityMatchingModelUpdate]]
        ],
    ) -> Union[EntityMatchingModel, List[EntityMatchingModel]]:
        """Update model

        Args:
            item (Union[EntityMatchingModel,EntityMatchingModelUpdate,List[Union[EntityMatchingModel,EntityMatchingModelUpdate]]) : Model(s) to update
        """
        return self._update_multiple(items=item)

    def list(self, filter: Dict = None) -> EntityMatchingModelList:
        """List models

        Args:
            filter (dict): If not None, return models with parameter values that matches what is specified in the filter.

        Returns:
            EntityMatchingModelList: List of models."""
        filter = {utils._auxiliary.to_camel_case(k): v for k, v in (filter or {}).items() if v is not None}
        models = self._camel_post("/list", json={"filter": filter}).json()["items"]
        return EntityMatchingModelList(
            [self._LIST_CLASS._RESOURCE._load(model, cognite_client=self._cognite_client) for model in models]
        )

    def list_jobs(self) -> EntityMatchingModelList:
        """List jobs

        Returns:
            EntityMatchingModelList: List of jobs."""
        return EntityMatchingModelList(
            [
                self._LIST_CLASS._RESOURCE._load(model, cognite_client=self._cognite_client)
                for model in self._camel_get("/jobs").json()["items"]
            ]
        )

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        """Delete models

        Args:
            id (Union[int, List[int]): Id or list of ids
            external_id (Union[str, List[str]]): External ID or list of external ids"""
        self._delete_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def fit(
        self,
        match_from: List[Union[Dict, CogniteResource]],
        match_to: List[Union[Dict, CogniteResource]],
        true_matches: List[Tuple[int, int]] = None,
        keys_from_to: List[Tuple[str, str]] = None,
        feature_type: str = None,
        classifier: str = None,
        complete_missing: bool = False,
        name: str = None,
        description: str = None,
        external_id: str = None,
    ) -> EntityMatchingModel:
        """Fit entity matching model.

        Args:
            match_from: entities to match from, should have an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list)
            match_to: entities to match to, should have an 'id' field.  Tolerant to passing more than is needed or used.
            true_matches: Known valid matches given as a list of (id_from,id_to). If omitted, uses an unsupervised model.
            keys_from_to: List of (from,to) keys to use in matching. Default in the API is [('name','name')]
            feature_type (str): feature type that defines the combination of features used, see API docs for details.
            classifier (str): classifier used in training. Currently undocumented in API.
            complete_missing (bool): whether missing data in keyFrom or keyTo should return error or be filled in with an empty string. Currently undocumented in API.
            name (str): Optional user-defined name of model.
            description (str): Optional user-defined description of model.
            external_id (str): Optional external id. Must be unique within the project.
        Returns:
            EntityMatchingModel: Resulting queued model."""
        if keys_from_to:
            keys_from_to = [{"keyFrom": f, "keyTo": t} for f, t in keys_from_to]
        if true_matches:
            true_matches = list(true_matches)

        response = self._camel_post(
            context_path="/fit",
            json=dict(
                match_from=EntityMatchingModel.dump_entities(match_from),
                match_to=EntityMatchingModel.dump_entities(match_to),
                true_matches=true_matches,
                keys_from_to=keys_from_to,
                feature_type=feature_type,
                classifier=classifier,
                complete_missing=complete_missing,
                name=name,
                description=description,
                external_id=external_id,
            ),
        )
        return self._LIST_CLASS._RESOURCE._load(response.json(), cognite_client=self._cognite_client)

    def predict(
        self,
        match_from: Optional[List[Dict]] = None,
        match_to: Optional[List[Dict]] = None,
        num_matches=1,
        score_threshold=None,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
    ) -> ContextualizationJob:
        """Predict entity matching. NB. blocks and waits for the model to be ready if it has been recently created.

        Args:
            match_from: entities to match from, does not need an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list). If omitted, will use data from fit.
            match_to: entities to match to, does not need an 'id' field.  Tolerant to passing more than is needed or used. If omitted, will use data from fit.
            num_matches (int): number of matches to return for each item.
            score_threshold (float): only return matches with a score above this threshold
            complete_missing (bool): whether missing data in keyFrom or keyTo should be filled in with an empty string.
            id: ids of the model to use.
            external_id: external ids of the model to use.
        Returns:
            ContextualizationJob: object which can be used to wait for and retrieve results."""
        return self.retrieve(
            id=id, external_id=external_id
        ).predict(  # could call predict directly but this is friendlier
            match_from=EntityMatchingModel.dump_entities(match_from),
            match_to=EntityMatchingModel.dump_entities(match_to),
            num_matches=num_matches,
            score_threshold=score_threshold,
        )

    def refit(
        self, true_matches: List[Tuple[int, int]], id: Optional[int] = None, external_id: Optional[str] = None
    ) -> "EntityMatchingModel":
        """Re-fits an entity matching model, using the combination of the old and new true matches.

        Args:
            true_matches: Updated known valid matches given as a list of (id_from,id_to).
            id: ids of the model to use.
            external_id: external ids of the model to use.
        Returns:
            EntityMatchingModel: new model refitted to true_matches."""
        return self.retrieve(id=id, external_id=external_id).refit(true_matches=true_matches)

    def create_rules(self, matches: List[Dict]) -> ContextualizationJob:
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a list of dictionaries with 'input', 'predicted' and (optionally) 'score'

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/rules", items=matches)
