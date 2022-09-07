from typing import Any, Dict, List, Union, cast

from cognite.client.data_classes._base import (
    CogniteFilter,
    CogniteListUpdate,
    CogniteObjectUpdate,
    CognitePrimitiveUpdate,
    CogniteResource,
    CogniteResourceList,
    CogniteUpdate,
)


class AlertChannel(CogniteResource):
    """Alert channel"""

    def __init__(
        self,
        external_id: str = None,
        id: int = None,
        name: str = None,
        parent_id: int = None,
        parent_external_id: str = None,
        description: str = None,
        metadata: Dict[str, str] = None,
        cognite_client: "CogniteClient" = None,
    ):
        self.external_id = external_id
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.parent_external_id = parent_external_id
        self.description = description
        self.metadata = metadata
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertChannelUpdate(CogniteUpdate):
    """Changes will be applied to alerting channel.

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveAlertChannelUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "AlertChannelUpdate":
            return self._set(value)

    class _ObjectAlertChannelUpdate(CogniteObjectUpdate):
        def set(self, value: Dict) -> "AlertChannelUpdate":
            return self._set(value)

        def add(self, value: Dict) -> "AlertChannelUpdate":
            return self._add(value)

        def remove(self, value: List) -> "AlertChannelUpdate":
            return self._remove(value)

    class _ListAlertChannelUpdate(CogniteListUpdate):
        def set(self, value: List) -> "AlertChannelUpdate":
            return self._set(value)

        def add(self, value: List) -> "AlertChannelUpdate":
            return self._add(value)

        def remove(self, value: List) -> "AlertChannelUpdate":
            return self._remove(value)

    @property
    def external_id(self) -> "_PrimitiveAlertChannelUpdate":
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "externalId")

    @property
    def name(self) -> "_PrimitiveAlertChannelUpdate":
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "name")

    @property
    def description(self) -> "_PrimitiveAlertChannelUpdate":
        return AlertChannelUpdate._PrimitiveAlertChannelUpdate(self, "description")

    @property
    def metadata(self) -> "_ObjectAlertChannelUpdate":
        return AlertChannelUpdate._ObjectAlertChannelUpdate(self, "metadata")


class AlertChannelList(CogniteResourceList):
    _RESOURCE = AlertChannel
    _UPDATE = AlertChannelUpdate
    _ASSERT_CLASSES = True


class AlertChannelFilter(CogniteFilter):
    """Filter on alert channels with strict matching."""

    def __init__(
        self,
        external_ids: List[str] = None,
        ids: List[int] = None,
        parent_ids: List[str] = None,
        metadata: Dict[str, str] = None,
        cognite_client: "CogniteClient" = None,
    ):
        self.external_ids = external_ids
        self.ids = ids
        self.parent_ids = parent_ids
        self.metadata = metadata
        self._cognite_client = cast("CogniteClient", cognite_client)


class Alert(CogniteResource):
    """Alert"""

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        timestamp: int = None,
        channel_id: int = None,
        channel_external_id: str = None,
        source: str = None,
        value: str = None,
        level: str = None,
        metadata: Dict[str, str] = None,
        acknowledged: bool = None,
        closed: bool = None,
        cognite_client: "CogniteClient" = None,
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
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertList(CogniteResourceList):
    _RESOURCE = Alert
    _UPDATE = None
    _ASSERT_CLASSES = False


class AlertFilter(CogniteFilter):
    """Filter on alerts with strict matching."""

    def __init__(
        self,
        ids: List[int] = None,
        external_ids: List[str] = None,
        channel_ids: List[int] = None,
        channel_external_ids: List[int] = None,
        closed: bool = None,
        start_time: int = None,
        end_time: int = None,
        cognite_client: "CogniteClient" = None,
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
        id: int = None,
        external_id: str = None,
        metadata: Dict[str, str] = None,
        email: str = None,
        cognite_client: "CogniteClient" = None,
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
        id: int = None,
        external_id: str = None,
        channel_id: int = None,
        channel_external_id: str = None,
        subscriber_id: int = None,
        subscriber_external_id: str = None,
        cognite_client: "CogniteClient" = None,
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
        id: int = None,
        external_id: str = None,
        channel_id: int = None,
        channel_external_id: str = None,
        subscriber_id: int = None,
        subscriber_external_id: str = None,
        metadata: Dict[str, str] = None,
        cognite_client: "CogniteClient" = None,
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
