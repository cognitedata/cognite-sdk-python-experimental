from typing import Dict, List, Optional, Tuple, Union

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource
from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import (
    ContextualizationJob,
    EntityMatchingModel,
    EntityMatchingModelList,
    EntityMatchingModelUpdate,
    EntityMatchingPipeline,
    EntityMatchingPipelineList,
    EntityMatchingPipelineRun,
    EntityMatchingPipelineRunList,
    EntityMatchingPipelineUpdate,
    convert_true_match,
)


class EntityMatchingPipelineRunsAPI(ContextAPI):
    _RESOURCE_PATH = EntityMatchingPipeline._RESOURCE_PATH + "/run"
    _LIST_CLASS = EntityMatchingPipelineRunList

    def retrieve(self, id: int) -> EntityMatchingPipelineRun:
        """Retrieve pipeline run

        Args:
            id: id of the pipeline run to retrieve.

        Returns:
            EntityMatchingPipelineRun: object which can be used to wait for and retrieve results."""
        return self._retrieve(id=id)

    def list(self, id=None, external_id=None, limit=100) -> EntityMatchingPipelineRunList:
        """List pipeline runs

        Args:
            id: id of the pipeline to retrieve runs for.
            external_id: external id of the pipeline to retrieve runs for.
            limit (int, optional): Maximum number of items to return. Defaults to 100. Set to -1, float("inf") or None to return all items.

        Returns:
            EntityMatchingPipelineRunList: list of pipeline runs"""
        runs = self._camel_post("/list", json={"id": id, "externalId": external_id, "limit": limit}).json()["items"]
        return EntityMatchingPipelineRunList._load(runs, cognite_client=self._cognite_client)

    def retrieve_latest(
        self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None
    ) -> Union[EntityMatchingPipelineRun, EntityMatchingPipelineRunList]:
        """List latest pipeline run for pipelines. Note that pipelines without a run are not returned, so output may not align with input.

        Args:
            id: id or list of ids of the pipelines to retrieve the latest run for.
            external_id: external id or list of external ids of the pipelines to retrieve the latest run for.

        Returns:
            Union[EntityMatchingPipelineRun,EntityMatchingPipelineRunList]: list of latest pipeline runs, or a single object if a single id was given and the run was found"""
        all_ids = self._process_ids(id, external_id, wrap_ids=True)
        is_single_id = self._is_single_identifier(id, external_id)
        runs = self._camel_post("/latest", json={"items": all_ids}).json()["items"]
        if is_single_id and runs:
            return EntityMatchingPipelineRun._load(runs[0], cognite_client=self._cognite_client)
        return EntityMatchingPipelineRunList._load(runs, cognite_client=self._cognite_client)


class EntityMatchingPipelinesAPI(ContextAPI):
    _RESOURCE_PATH = EntityMatchingPipeline._RESOURCE_PATH
    _LIST_CLASS = EntityMatchingPipelineList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runs = EntityMatchingPipelineRunsAPI(*args, **kwargs)

    def create(self, pipeline: EntityMatchingPipeline) -> EntityMatchingPipeline:
        """Create an Entity Matching Pipeline.
        Args:
            pipeline (EntityMatchingPipeline): pipeline to create.

        Returns:
            EntityMatchingPipeline: created pipeline."""
        result = self._camel_post("", json=pipeline.dump()).json()
        return EntityMatchingPipeline._load(result, cognite_client=self._cognite_client)

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[EntityMatchingPipeline]:
        """Retrieve pipeline

            Args:
                id: id of the pipeline to retrieve.
                external_id: external id of the pipeline to retrieve.

            Returns:
                EntityMatchingPipeline: Model requested."""
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def retrieve_multiple(
        self, ids: Optional[List[int]] = None, external_ids: Optional[List[str]] = None
    ) -> EntityMatchingPipelineList:
        """Retrieve models

        Args:
            ids: ids of the pipelines retrieve.
            external_ids: external ids of the pipelines to retrieve.

        Returns:
            EntityMatchingModelList: Models requested."""
        utils._auxiliary.assert_type(ids, "id", [List], allow_none=True)
        utils._auxiliary.assert_type(external_ids, "external_id", [List], allow_none=True)
        return self._retrieve_multiple(ids=ids, external_ids=external_ids, wrap_ids=True)

    def list(self, limit=100) -> EntityMatchingPipelineList:
        """List pipelines
        Args:
            limit (int, optional): Maximum number of items to return. Defaults to 25. Set to -1, float("inf") or None to return all items.

        Returns:
            EntityMatchingModelList: List of pipelines."""
        pipelines = self._camel_post("/list", json={"limit": limit}).json()["items"]
        return EntityMatchingPipelineList._load(pipelines, cognite_client=self._cognite_client)

    def run(self, id: int = None, external_id: str = None) -> EntityMatchingPipelineRun:
        """Run pipeline

        Args:
            id: id of the pipeline to run.
            external_id: external id of the pipeline to run.

        Returns:
            EntityMatchingPipelineRun: object which can be used to wait for and retrieve results."""
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._run_job(job_path="/run", id=id, external_id=external_id, job_cls=EntityMatchingPipelineRun)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        """Delete pipelines

        Args:
            id (Union[int, List[int]): Id or list of ids
            external_id (Union[str, List[str]]): External ID or list of external ids"""
        self._delete_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def update(
        self,
        item: Union[
            EntityMatchingPipeline,
            EntityMatchingPipelineUpdate,
            List[Union[EntityMatchingPipeline, EntityMatchingPipelineUpdate]],
        ],
    ) -> Union[EntityMatchingPipeline, List[EntityMatchingPipeline]]:
        """Update model

        Args:
            items (Union[EntityMatchingPipeline, EntityMatchingPipelineUpdate, List[Union[EntityMatchingPipeline, EntityMatchingPipelineUpdate]]]) : Pipeline(s) to update
        """
        return self._update_multiple(items=item)


class EntityMatchingAPI(ContextAPI):
    _RESOURCE_PATH = EntityMatchingModel._RESOURCE_PATH
    _LIST_CLASS = EntityMatchingModelList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipelines = EntityMatchingPipelinesAPI(*args, **kwargs)

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

    def list(self, filter: Dict = None, limit=100) -> EntityMatchingModelList:
        """List models

        Args:
            filter (dict): If not None, return models with parameter values that matches what is specified in the filter.
            limit (int, optional): Maximum number of items to return. Defaults to 100. Set to -1, float("inf") or None to return all items.

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
        sources: List[Union[Dict, CogniteResource]],
        targets: List[Union[Dict, CogniteResource]],
        true_matches: List[Union[Dict, Tuple[Union[int, str], Union[int, str]]]] = None,
        match_fields: List[Tuple[str, str]] = None,
        feature_type: str = None,
        classifier: str = None,
        ignore_missing_fields: bool = False,
        name: str = None,
        description: str = None,
        external_id: str = None,
    ) -> EntityMatchingModel:
        """Fit entity matching model.
        Note: All users on this CDF subscription with assets read-all capability in the project, are able to access the data sent to this endpoint.

        Args:
            sources: entities to match from, should have an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list)
            targets: entities to match to, should have an 'id' field.  Tolerant to passing more than is needed or used.
            id_field (str): use 'id' or 'external_id' as the id field to match resources
            true_matches: Known valid matches given as a list of dicts with keys 'sourceId', 'sourceExternalId', 'sourceId', 'sourceExternalId'). If omitted, uses an unsupervised model.
             A tuple can be used instead of the dictionary for convenience, interpreted as id/externalId based on type.
            match_fields: List of (from,to) keys to use in matching. Default in the API is [('name','name')]
            feature_type (str): feature type that defines the combination of features used, see API docs for details.
            classifier (str): classifier used in training. Currently undocumented in API.
            ignore_missing_fields (bool): whether missing data in keyFrom or keyTo should return error or be filled in with an empty string. Currently undocumented in API.
            name (str): Optional user-defined name of model.
            description (str): Optional user-defined description of model.
            external_id (str): Optional external id. Must be unique within the project.
        Returns:
            EntityMatchingModel: Resulting queued model."""

        if match_fields:
            match_fields = [ft if isinstance(ft, dict) else {"source": ft[0], "target": ft[1]} for ft in match_fields]
        if true_matches:
            true_matches = [convert_true_match(true_match) for true_match in true_matches]
        response = self._camel_post(
            context_path="/",
            json=dict(
                sources=EntityMatchingModel.dump_entities(sources),
                targets=EntityMatchingModel.dump_entities(targets),
                true_matches=true_matches,
                match_fields=match_fields,
                feature_type=feature_type,
                classifier=classifier,
                ignore_missing_fields=ignore_missing_fields,
                name=name,
                description=description,
                external_id=external_id,
            ),
        )
        return self._LIST_CLASS._RESOURCE._load(response.json(), cognite_client=self._cognite_client)

    def predict(
        self,
        sources: Optional[List[Dict]] = None,
        targets: Optional[List[Dict]] = None,
        num_matches=1,
        score_threshold=None,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
    ) -> ContextualizationJob:
        """Predict entity matching. NB. blocks and waits for the model to be ready if it has been recently created.
        Note: All users on this CDF subscription with assets read-all capability in the project, are able to access the
        data sent to this endpoint.

        Args:
            sources: entities to match from, does not need an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list). If omitted, will use data from fit.
            targets: entities to match to, does not need an 'id' field.  Tolerant to passing more than is needed or used. If omitted, will use data from fit.
            num_matches (int): number of matches to return for each item.
            score_threshold (float): only return matches with a score above this threshold
            ignore_missing_fields (bool): whether missing data in keyFrom or keyTo should be filled in with an empty string.
            id: ids of the model to use.
            external_id: external ids of the model to use.
        Returns:
            ContextualizationJob: object which can be used to wait for and retrieve results."""
        return self.retrieve(
            id=id, external_id=external_id
        ).predict(  # could call predict directly but this is friendlier
            sources=EntityMatchingModel.dump_entities(sources),
            targets=EntityMatchingModel.dump_entities(targets),
            num_matches=num_matches,
            score_threshold=score_threshold,
        )

    def refit(
        self,
        true_matches: List[Union[Dict, Tuple[Union[int, str], Union[int, str]]]],
        id: Optional[int] = None,
        external_id: Optional[str] = None,
    ) -> "EntityMatchingModel":
        """Re-fits an entity matching model, using the combination of the old and new true matches.
        Note: All users on this CDF subscription with assets read-all capability in the project, are able to access the data sent to this endpoint.

        Args:
            true_matches: Updated known valid matches given as a list of dicts with keys 'fromId', 'fromExternalId', 'toId', 'toExternalId').
                 A tuple can be used instead of the dictionary for convenience, interpreted as id/externalId based on type.
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
