from typing import Any, Dict, List, Union, cast

from cognite.client.data_classes._base import CogniteFilter, CogniteResource, CogniteResourceList


class AlertChannel(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        name: str = None,
        parent_id: int = None,
        parent_external_id: str = None,
        description: str = None,
        metadata: Dict[str, str] = None,
        cognite_client: "CogniteClient" = None,
    ):
        self.external_id = external_id
        self.name = name
        self.parent_id = parent_id
        self.parent_external_id = parent_external_id
        self.description = description
        self.metadata = metadata
        # self.id = id
        self._cognite_client = cast("CogniteClient", cognite_client)


class AlertChannelList(CogniteResourceList):
    _RESOURCE = AlertChannel


class AlertChannelFilter(CogniteFilter):
    """Filter on alert channels with strict matching.
    Args:
    """

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
    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        timestamp: str = None,
        channel_id: int = None,
        channel_external_id: int = None,
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


class AlertFilter(CogniteFilter):
    """Filter on alerts with strict matching.
    Args:
    """

    def __init__(
        self,
        ids: List[int] = None,
        external_ids: List[str] = None,
        channel_ids: List[int] = None,
        channel_external_ids: List[int] = None,
        closed: bool = None,
        start_time: str = None,
        end_time: str = None,
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