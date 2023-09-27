import json
from typing import Any, Dict, List, Optional, Type, Union

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._text import to_snake_case
from typing_extensions import Self


class HostedExtractorsSource(CogniteResource):
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
    ) -> Union[
        "HostedExtractorsEventHubSource",
        "HostedExtractorsMqttSource",
        "HostedExtractorsRestSource",
        "HostedExtractorsKafkaSource",
    ]:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        if resource["type"] == "mqtt3" or resource["type"] == "mqtt5":
            return HostedExtractorsMqttSource._load(resource, cognite_client)
        elif resource["type"] == "eventhub":
            return HostedExtractorsEventHubSource._load(resource, cognite_client)
        elif resource["type"] == "rest":
            return HostedExtractorsRestSource._load(resource, cognite_client)
        elif resource["type"] == "kafka":
            return HostedExtractorsKafkaSource._load(resource, cognite_client)
        else:
            raise ValueError(f"Unknown source type {resource['type']}")


class HostedExtractorsMqttSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = None,
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
        self.use_tls = use_tls
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def _load(cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsMqttSource(**data, cognite_client=cognite_client)


class HostedExtractorsEventHubSource(HostedExtractorsSource):
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
        return HostedExtractorsEventHubSource(**data, cognite_client=cognite_client)


class HostedExtractorsRestSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: str = None,
        port: int = None,
        interval: str = None,
        pagination: Dict[str, Any] = None,
        incremental_load: Dict[str, Any] = None,
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
        self.interval = interval
        self.pagination = pagination
        self.incremental_load = incremental_load

    @classmethod
    def _load(cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsRestSource(**data, cognite_client=cognite_client)


class HostedExtractorsKafkaSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str = None,
        type: str = None,
        host: List[str] = None,
        use_tls: bool = None,
        username: str = None,
        password: str = None,
        ca_certificate: str = None,
        auth_certificate: str = None,
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
        self.use_tls = use_tls
        self.username = username
        self.password = password
        self.ca_certificate = ca_certificate
        self.auth_certificate = auth_certificate

    @classmethod
    def _load(cls: Type[Self], resource: Union[Dict, str], cognite_client: "CogniteClient" = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsKafkaSource(**data, cognite_client=cognite_client)


class HostedExtractorsJob(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        format: Dict[str, Any] = None,
        config: Dict[str, Any] = None,
        status: str = None,
        target_status: str = None,
        source_id: str = None,
        destination_id: str = None,
        created_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.format = format
        self.config = config
        self.status = status
        self.target_status = target_status
        self.source_id = source_id
        self.destination_id = destination_id
        self.created_time = created_time
        self.cognite_client = cognite_client


class HostedExtractorsDestination(CogniteResource):
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


class HostedExtractorsSourceList(CogniteResourceList):
    _RESOURCE = HostedExtractorsSource


class HostedExtractorsJobList(CogniteResourceList):
    _RESOURCE = HostedExtractorsJob


class HostedExtractorsDestinationList(CogniteResourceList):
    _RESOURCE = HostedExtractorsDestination
