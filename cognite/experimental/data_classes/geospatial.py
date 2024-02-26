from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, cast

from cognite.client import utils
from cognite.client.data_classes._base import (
    CogniteResource,
    CogniteResourceList,
    ExternalIDTransformerMixin,
    WriteableCogniteResource,
    WriteableCogniteResourceList,
)

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class FeatureTypeCore(WriteableCogniteResource["FeatureTypeWrite"], ABC):
    def __init__(
        self,
        external_id: str | None = None,
        data_set_id: int | None = None,
        properties: dict[str, Any] | None = None,
        search_spec: dict[str, Any] | None = None,
        partitions: list[dict[str, Any]] | None = None,
    ) -> None:
        self.external_id = external_id
        self.data_set_id = data_set_id
        self.properties = properties
        self.search_spec = search_spec
        self.partitions = partitions


class FeatureTypeWrite(FeatureTypeCore):
    def __init__(
        self,
        external_id: str,
        properties: dict[str, Any],
        data_set_id: int | None = None,
        search_spec: dict[str, Any] | None = None,
        partitions: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            external_id=external_id,
            data_set_id=data_set_id,
            properties=properties,
            search_spec=search_spec,
            partitions=partitions,
        )

    @classmethod
    def _load(cls, resource: dict[str, Any], cognite_client: CogniteClient | None = None) -> FeatureTypeWrite:
        return cls(
            external_id=resource["externalId"],
            properties=resource["properties"],
            data_set_id=resource.get("dataSetId"),
            search_spec=resource.get("searchSpec"),
            partitions=resource.get("partitions"),
        )

    def as_write(self) -> FeatureTypeWrite:
        """Returns this FeatureTypeWrite instance."""
        return self


class FeatureType(FeatureTypeCore):
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
        super().__init__(
            external_id=external_id,
            data_set_id=data_set_id,
            properties=properties,
            search_spec=search_spec,
            partitions=partitions,
        )
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cast("CogniteClient", cognite_client)

    @classmethod
    def _load(cls, resource: dict[str, Any], cognite_client: CogniteClient | None = None) -> FeatureType:
        return cls(
            external_id=resource.get("externalId"),
            data_set_id=resource.get("dataSetId"),
            created_time=resource.get("createdTime"),
            last_updated_time=resource.get("lastUpdatedTime"),
            properties=resource.get("properties"),
            search_spec=resource.get("searchSpec"),
            partitions=resource.get("partitions"),
            cognite_client=cognite_client,
        )

    def as_write(self) -> FeatureTypeWrite:
        """Returns a write version of this feature type."""
        if self.external_id is None or self.properties is None:
            raise ValueError("External ID and properties must be set to create a feature type")

        return FeatureTypeWrite(
            external_id=self.external_id,
            properties=self.properties,
            data_set_id=self.data_set_id,
            search_spec=self.search_spec,
            partitions=self.partitions,
        )


class FeatureTypeWriteList(CogniteResourceList[FeatureTypeWrite], ExternalIDTransformerMixin):
    _RESOURCE = FeatureTypeWrite


class FeatureTypeList(WriteableCogniteResourceList[FeatureTypeWrite, FeatureType]):
    _RESOURCE = FeatureType

    def as_write(self) -> FeatureTypeWriteList:
        return FeatureTypeWriteList(
            [feature_type.as_write() for feature_type in self], cognite_client=self._get_cognite_client()
        )


class MvpMappingsDefinitionCore(WriteableCogniteResource["MvpMappingsDefinitionWrite"], ABC):
    """MVT mappings definition"""

    def __init__(
        self,
        external_id: str | None = None,
        mappings: list[dict[str, Any]] | None = None,
    ):
        self.external_id = external_id
        self.mappings = mappings


class MvpMappingsDefinitionWrite(MvpMappingsDefinitionCore):
    """MVT mappings definition"""

    def __init__(
        self,
        external_id: str | None = None,
        mappings: list[dict[str, Any]] | None = None,
    ):
        super().__init__(external_id, mappings)

    def as_write(self) -> MvpMappingsDefinitionWrite:
        return self


class MvpMappingsDefinition(MvpMappingsDefinitionCore):
    """MVT mappings definition"""

    def __init__(
        self,
        external_id: str | None = None,
        mappings: list[dict[str, Any]] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        super().__init__(external_id, mappings)
        self._cognite_client = cast("CogniteClient", cognite_client)

    def as_write(self) -> MvpMappingsDefinitionWrite:
        """Returns this Table as a TableWrite"""
        return MvpMappingsDefinitionWrite(
            external_id=self.external_id,
            mappings=self.mappings,
        )


class MvpMappingsDefinitionWriteList(CogniteResourceList[MvpMappingsDefinitionWrite]):
    _RESOURCE = MvpMappingsDefinitionWrite


class MvpMappingsDefinitionList(WriteableCogniteResourceList[MvpMappingsDefinitionWrite, MvpMappingsDefinition]):
    _RESOURCE = MvpMappingsDefinition

    def as_write(self) -> MvpMappingsDefinitionWriteList:
        return MvpMappingsDefinitionWriteList(
            [mvp_mappings_definition.as_write() for mvp_mappings_definition in self.data],
            cognite_client=self._get_cognite_client(),
        )


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
