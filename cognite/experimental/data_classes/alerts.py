from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from cognite.client.data_classes._base import (
    CogniteFilter,
    CogniteListUpdate,
    CogniteObjectUpdate,
    CognitePrimitiveUpdate,
    CogniteResource,
    CogniteResourceList,
    CogniteUpdate,
)

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class AlertChannel(CogniteResource):
    """Alert channel"""

    def __init__(
        self,
        external_id: str | None = None,
        id: int | None = None,
        name: str | None = None,
        parent_id: int | None = None,
        parent_external_id: str | None = None,
        description: str | None = None,
        metadata: dict[str, str] | None = None,
        alert_rules: dict[str, dict[str, str]] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.external_id = external_id
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.parent_external_id = parent_external_id
        self.description = description
        self.metadata = metadata
        self.alert_rules = alert_rules
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertChannelUpdate(CogniteUpdate):
    """Changes will be applied to alerting channel.

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveAlertChannelUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> AlertChannelUpdate:
            return self._set(value)

    class _ObjectAlertChannelUpdate(CogniteObjectUpdate):
        def set(self, value: dict) -> AlertChannelUpdate:
            return self._set(value)

        def add(self, value: dict) -> AlertChannelUpdate:
            return self._add(value)

        def remove(self, value: list) -> AlertChannelUpdate:
            return self._remove(value)

    class _ListAlertChannelUpdate(CogniteListUpdate):
        def set(self, value: list) -> AlertChannelUpdate:
            return self._set(value)

        def add(self, value: list) -> AlertChannelUpdate:
            return self._add(value)

        def remove(self, value: list) -> AlertChannelUpdate:
            return self._remove(value)

    @property
    def external_id(self) -> _PrimitiveAlertChannelUpdate:
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "externalId")

    @property
    def name(self) -> _PrimitiveAlertChannelUpdate:
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "name")

    @property
    def description(self) -> _PrimitiveAlertChannelUpdate:
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "description")

    @property
    def metadata(self) -> _ObjectAlertChannelUpdate:
        return AlertChannelUpdate._ObjectAlertChannelUpdate(self, "metadata")


class AlertChannelList(CogniteResourceList):
    _RESOURCE = AlertChannel
    _UPDATE = AlertChannelUpdate
    _ASSERT_CLASSES = True


class AlertChannelFilter(CogniteFilter):
    """Filter on alert channels with strict matching."""

    def __init__(
        self,
        external_ids: list[str] | None = None,
        ids: list[int] | None = None,
        parent_ids: list[str] | None = None,
        metadata: dict[str, str] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.external_ids = external_ids
        self.ids = ids
        self.parent_ids = parent_ids
        self.metadata = metadata
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertTriggeredPoint:
    """Triggered point, will be deduplicated into one or more alerts"""

    def __init__(self, triggered: int, timestamp: int):
        self.timestamp = timestamp
        self.triggered = triggered


class Alert(CogniteResource):
    """Alert"""

    def __init__(
        self,
        id: int | None = None,
        external_id: str | None = None,
        timestamp: int | None = None,
        channel_id: int | None = None,
        channel_external_id: str | None = None,
        source: str | None = None,
        value: str | None = None,
        level: str | None = None,
        metadata: dict[str, str] | None = None,
        acknowledged: bool | None = None,
        closed: bool | None = None,
        triggered_points: list[AlertTriggeredPoint] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.id = id
        self.external_id = external_id
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.channel_external_id = channel_external_id
        self.source = source
        self.value = value
        self.level = level
        self.metadata = metadata
        self.acknowledged = acknowledged
        self.closed = closed
        self.triggered_points = triggered_points
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertList(CogniteResourceList):
    _RESOURCE = Alert
    _UPDATE = None
    _ASSERT_CLASSES = False


class AlertFilter(CogniteFilter):
    """Filter on alerts with strict matching."""

    def __init__(
        self,
        ids: list[int] | None = None,
        external_ids: list[str] | None = None,
        channel_ids: list[int] | None = None,
        channel_external_ids: list[int] | None = None,
        closed: bool | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.ids = ids
        self.external_ids = external_ids
        self.channel_ids = channel_ids
        self.channel_external_ids = channel_external_ids
        self.closed = closed
        self.start_time = start_time
        self.end_time = end_time
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertSubscriber(CogniteResource):
    """Alert subscriber"""

    def __init__(
        self,
        id: int | None = None,
        external_id: str | None = None,
        metadata: dict[str, str] | None = None,
        email: str | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.id = id
        self.external_id = external_id
        self.metadata = metadata
        self.email = email
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertSubscriberList(CogniteResourceList):
    _RESOURCE = AlertSubscriber
    _UPDATE = None
    _ASSERT_CLASSES = False


class AlertSubscriptionDelete(CogniteResource):
    def __init__(
        self,
        id: int | None = None,
        external_id: str | None = None,
        channel_id: int | None = None,
        channel_external_id: str | None = None,
        subscriber_id: int | None = None,
        subscriber_external_id: str | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.id = id
        self.external_id = external_id
        self.channel_id = channel_id
        self.channel_external_id = channel_external_id
        self.subscriber_id = subscriber_id
        self.subscriber_external_id = subscriber_external_id
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertSubscription(CogniteResource):
    """Alert subscription"""

    def __init__(
        self,
        id: int | None = None,
        external_id: str | None = None,
        channel_id: int | None = None,
        channel_external_id: str | None = None,
        subscriber_id: int | None = None,
        subscriber_external_id: str | None = None,
        metadata: dict[str, str] | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.id = id
        self.external_id = external_id
        self.channel_id = channel_id
        self.channel_external_id = channel_external_id
        self.subscriber_id = subscriber_id
        self.subscriber_external_id = subscriber_external_id
        self.metadata = metadata
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertSubscriptionList(CogniteResourceList):
    _RESOURCE = AlertSubscription
    _UPDATE = None
    _ASSERT_CLASSES = False
