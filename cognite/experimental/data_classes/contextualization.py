import copy
import math
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import (
    CognitePrimitiveUpdate,
    CogniteResource,
    CogniteResourceList,
    CogniteUpdate,
)
from cognite.client.exceptions import ModelFailedException
from cognite.client.utils._auxiliary import to_camel_case
from typing_extensions import TypedDict


class EntityMatchingPipelineRun(ContextualizationJob):
    def __init__(self, pipeline_id=None, **kwargs):
        super().__init__(**kwargs)
        self.pipeline_id = pipeline_id
        self._status_path = "/context/entitymatching/pipelines/run/"  # since we can list this, would like .result even if we didn't this via .run

    @property
    def suggested_rules(self):
        """List of suggested rules. Depends on .result and may block"""
        return self.result["suggestedRules"]

    @property
    def matches(self):
        """List of matches. Depends on .result and may block"""
        return self.result["matches"]


class EntityMatchingPipelineRunList(CogniteResourceList):
    _RESOURCE = EntityMatchingPipelineRun
    _UPDATE = None
    _ASSERT_CLASSES = False


class EntityMatchingPipeline(CogniteResource):
    _RESOURCE_PATH = "/context/entitymatching/pipelines"
    _STATUS_PATH = _RESOURCE_PATH + "/"

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        name: str = None,
        description: str = None,
        model_parameters: Dict = None,
        sources: Dict = None,
        targets: Dict = None,
        true_matches: List = None,
        rejected_matches: List = None,
        confirmed_matches: List = None,
        use_existing_matches: bool = None,
        relationships_label: str = None,
        score_threshold: float = None,
        schedule_interval: int = None,
        rules: List = None,
        status=None,
        error_message=None,
        created_time=None,
        start_time=None,
        status_time=None,
        cognite_client=None,
    ):
        """
        The fields below can be filled when creating a pipeline. Other fields should be left empty, and return status information on successful creation and retrieval.
        Args:
            external_id, name, description: standard fields for a resource.
            model_parameters: a dictionary with fields `match_fields`, `feature_type`, `classifier`, as in the `fit` method for entity matching.
            sources, targets: a dictionary of the format {'resource': ..., 'dataSetIds': [{'id':...},{'externalId':...}]}
            true_matches: existing matches with reasonable certainty to use in training.
            confirmed_matches: user-confirmed certain matches which will be used to override any other results.
            rejected_matches: user-confirmed wrong results which will be used to blank output for a match result if it is one of these.
            use_existing_matches: If set, uses existing matches on resources as additional true_matches (but not confirmed_matches).
            relationships_label: If set, writes relationships with this label to the tenant (along with a pipeline-specific and general entity matching label). Requires whitelisting by auth.
            rules: list of matching rules
            schedule_interval: automatically schedule pipeline to be run every this many seconds.
        """

        self.id = id
        self.external_id = external_id
        self.name = name
        self.description = description
        self.model_parameters = model_parameters
        self.sources = sources
        self.targets = targets
        self.true_matches = true_matches
        self.confirmed_matches = confirmed_matches
        self.rejected_matches = rejected_matches
        self.use_existing_matches = use_existing_matches
        self.relationships_label = relationships_label
        self.score_threshold = score_threshold
        self.rules = rules
        self.schedule_interval = schedule_interval

        self.status = status
        self.created_time = created_time
        self.start_time = start_time
        self.status_time = status_time
        self.error_message = error_message

        self._cognite_client = cognite_client

    def run(self) -> EntityMatchingPipelineRun:
        return self._cognite_client.entity_matching.pipelines.run(id=self.id)

    def runs(self) -> EntityMatchingPipelineRunList:
        return self._cognite_client.entity_matching.pipelines.runs.list(id=self.id)

    def latest_run(self) -> EntityMatchingPipelineRun:
        return self._cognite_client.entity_matching.pipelines.runs.retrieve_latest(id=self.id)


class EntityMatchingPipelineUpdate(CogniteUpdate):  # not implemented yet
    """Changes applied to entity matching pipeline

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "EntityMatchingPipelineUpdate":
            return self._set(value)

    @property
    def name(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "name")

    @property
    def description(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "description")

    @property
    def model_parameters(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "modelParameters")

    @property
    def sources(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "sources")

    @property
    def targets(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "targets")

    @property
    def true_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "trueMatches")

    @property
    def confirmed_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "confirmedMatches")

    @property
    def rejected_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "rejectedMatches")

    @property
    def rules(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "rules")

    @property
    def score_threshold(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "scoreThreshold")

    @property
    def schedule_interval(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "scheduleInterval")


class EntityMatchingPipelineList(CogniteResourceList):
    _RESOURCE = EntityMatchingPipeline
    _UPDATE = EntityMatchingPipelineUpdate
