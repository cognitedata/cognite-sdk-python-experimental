from typing import Any, Dict, Optional

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class PlutoSource(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        port: Optional[int] = None,
        config: Dict[str, Any] = None,
        created_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.type = type
        self.host = host
        self.port = port
        self.config = config
        self.created_time = created_time
        self.cognite_client = cognite_client


class PlutoJob(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        topic_filter: str = None,
        format: Dict[str, Any] = None,
        status: str = None,
        target_status: str = None,
        source_id: str = None,
        destination_id: str = None,
        created_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.topic_filter = topic_filter
        self.format = format
        self.status = status
        self.target_status = target_status
        self.source_id = source_id
        self.destination_id = destination_id
        self.created_time = created_time
        self.cognite_client = cognite_client


class PlutoDestination(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        session_id: Optional[int] = None,
        created_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.type = type
        self.format = format
        self.session_id = session_id
        self.created_time = created_time
        self.cognite_client = cognite_client


class PlutoSourceList(CogniteResourceList):
    _RESOURCE = PlutoSource
    _ASSERT_CLASSES = False


class PlutoJobList(CogniteResourceList):
    _RESOURCE = PlutoJob
    _ASSERT_CLASSES = False


class PlutoDestinationList(CogniteResourceList):
    _RESOURCE = PlutoDestination
    _ASSERT_CLASSES = False
