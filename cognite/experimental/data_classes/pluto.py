import json
from typing import Any, Dict, Optional, Type, Union

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._text import to_snake_case
from typing_extensions import Self


class PlutoSource(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.type = type
        self.host = host
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.cognite_client = cognite_client

    @classmethod
    def _load(
        cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None
    ) -> Union["PlutoEventHubSource", "PlutoMqttSource"]:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        if resource["type"] == "mqtt3" or resource["type"] == "mqtt5":
            return PlutoMqttSource._load(resource, cognite_client)

        elif resource["type"] == "eventhub":
            return PlutoEventHubSource._load(resource, cognite_client)


class PlutoMqttSource(PlutoSource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        super().__init__(
            external_id=external_id,
            type=type,
            host=host,
            created_time=created_time,
            last_updated_time=last_updated_time,
            cognite_client=cognite_client,
        )
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def _load(cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return PlutoMqttSource(**data, cognite_client=cognite_client)


class PlutoEventHubSource(PlutoSource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        key_name: str = None,
        event_hub_name: str = None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        super().__init__(
            external_id=external_id,
            type=type,
            host=host,
            created_time=created_time,
            last_updated_time=last_updated_time,
            cognite_client=cognite_client,
        )
        self.key_name = key_name
        self.event_hub_name = event_hub_name

    @classmethod
    def _load(cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return PlutoEventHubSource(**data, cognite_client=cognite_client)


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


class PlutoJobList(CogniteResourceList):
    _RESOURCE = PlutoJob


class PlutoDestinationList(CogniteResourceList):
    _RESOURCE = PlutoDestination
