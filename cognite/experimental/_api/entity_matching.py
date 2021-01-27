from typing import Dict, List, Optional, Tuple, Union

from cognite.client import utils
from cognite.client._api.entity_matching import EntityMatchingAPI as EntityMatchingBaseAPI
from cognite.client.data_classes import (
    ContextualizationJob,
    EntityMatchingModel,
    EntityMatchingModelList,
    EntityMatchingModelUpdate,
)

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import (
    EntityMatchingPipeline,
    EntityMatchingPipelineList,
    EntityMatchingPipelineRun,
    EntityMatchingPipelineRunList,
    EntityMatchingPipelineUpdate,
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

    def _fix_update(self, item):
        def fix_rules(rules):
            rules = [rule if isinstance(rule, dict) else rule.dump(camel_case=True) for rule in rules]
            # strip fields that are returned by pipelines but not valid input
            rules = [
                {k: v for k, v in rule.items() if k not in {"numConflicts", "matches", "numOverlaps"}} for rule in rules
            ]
            return rules

        if isinstance(item, EntityMatchingPipeline):
            item.rules = fix_rules(item.rules)
        else:  # EntityMatchingPipelineUpdate
            update_obj = item._update_object.get("rules", None)
            if update_obj:
                update_obj["set"] = fix_rules(update_obj["set"])
        return item

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
        if isinstance(item, list):
            item = [self._fix_update(update) for update in item]
        else:
            item = self._fix_update(item)
        return self._update_multiple(items=item)


class EntityMatchingAPI(EntityMatchingBaseAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipelines = EntityMatchingPipelinesAPI(*args, **kwargs)

    def create_rules(self, matches: List[Dict]) -> ContextualizationJob:
        """Fit rules model.

        Args:
            matches: list of matches to create rules for, given as a list of dictionaries with 'input', 'predicted' and (optionally) 'score'

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/rules", json={"items": matches})
