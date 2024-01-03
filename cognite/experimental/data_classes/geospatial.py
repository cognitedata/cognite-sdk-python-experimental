from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._text import to_snake_case

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class FeatureType(CogniteResource):
    """A representation of a feature type in the geospatial api."""

    def __init__(
        self,
        external_id: str | None = None,
        data_set_id: int | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
        properties: dict[str, Any] | None = None,
        search_spec: dict[str, Any] | None = None,
        partitions: list[dict[str, Any]] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.external_id = external_id
        self.data_set_id = data_set_id
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.properties = properties
        self.search_spec = search_spec
        self.partitions = partitions
        self._cognite_client = cast("CogniteClient", cognite_client)

    @classmethod
    def _load(cls, resource: str | dict[str, Any], cognite_client: CogniteClient | None = None) -> FeatureType:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client=cognite_client)
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class FeatureTypeList(CogniteResourceList):
    _RESOURCE = FeatureType


class MvpMappingsDefinition(CogniteResource):
    """MVT mappings definition"""

    def __init__(
        self,
        external_id: str | None = None,
        mappings: list[dict[str, Any]] | None = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.mappings = mappings
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class MvpMappingsDefinitionList(CogniteResourceList):
    _RESOURCE = MvpMappingsDefinition
    _ASSERT_CLASSES = False


class ComputedItem(CogniteResource):
    """A representation of a computed item by the geospatial api."""

    def __init__(self, cognite_client=None, **properties):
        for key in properties:
            setattr(self, key, properties[key])
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class ComputedItemList(CogniteResourceList):
    _RESOURCE = ComputedItem
    _ASSERT_CLASSES = False


class ComputeOrder:
    """An order specification with respect to an expression."""

    def __init__(self, expression: dict[str, Any], direction: str):
        self.expression = expression
        self.direction = direction


class GeospatialTask(CogniteResource):
    """A geospatial background task."""

    def __init__(
        self,
        external_id: str | None = None,
        task_type: str | None = None,
        request: dict[str, Any] | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
        state: str | None = None,
        result: dict[str, Any] | None = None,
        events: dict[str, Any] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.external_id = external_id
        self.task_type = task_type
        self.request = request
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.state = state
        self.result = result
        self.events = events
        self._cognite_client = cast("CogniteClient", cognite_client)


class GeospatialTaskList(CogniteResourceList):
    """A list of geospatial background tasks."""

    _RESOURCE = GeospatialTask
