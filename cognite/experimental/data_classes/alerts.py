from typing import Dict, List, Union, cast

from cognite.client.data_classes._base import (
    CogniteFilter,
    CogniteResource,
    CogniteResourceList,
)


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
        self.id = id
        self._cognite_client = cast("CogniteClient", cognite_client)

    def to_pandas(self, camel_case=False):
        pass


class AlertChannelList(CogniteResourceList):
    _RESOURCE = AlertChannel
    _ASSERT_CLASSES = False

    @classmethod
    def _load(cls, resource_list: Union[List, str], cognite_client=None):
        loaded = super()._load(resource_list, cognite_client)
        loaded.data = sorted(loaded.data, key=lambda match: -match.score)  # sort matches from highest to lowest score
        return loaded

    def to_pandas(self, camel_case=False):
        pass


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
        # channel: AlertsChannel = None,
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
        # self.channel = channel
        self.source = source
        self.value = value
        self.level = level
        self.metadata = metadata
        self.acknowledged = acknowledged
        self.closed = closed
        self._cognite_client = cast("CogniteClient", cognite_client)

    def to_pandas(self, camel_case=False):
        pass


class AlertList(CogniteResourceList):
    _RESOURCE = Alert
    _ASSERT_CLASSES = False

    @classmethod
    def _load(cls, resource_list: Union[List, str], cognite_client=None):
        loaded = super()._load(resource_list, cognite_client)
        loaded.data = sorted(loaded.data, key=lambda match: -match.score)  # sort matches from highest to lowest score
        return loaded

    def to_pandas(self, camel_case=False):
        pass


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
