from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._text import to_snake_case

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class HostedExtractorsSource(CogniteResource):
    def __init__(
        self,
        external_id: str | None = None,
        type: str | None = None,
        host: str | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
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
        cls: type[Self], resource: dict | str, cognite_client: CogniteClient | None = None
    ) -> (
        HostedExtractorsEventHubSource
        | HostedExtractorsMqttSource
        | HostedExtractorsRestSource
        | HostedExtractorsKafkaSource
    ):
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
        external_id: str | None = None,
        type: str | None = None,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
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
    def _load(cls: type[Self], resource: dict | str, cognite_client: CogniteClient = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsMqttSource(**data, cognite_client=cognite_client)


class HostedExtractorsEventHubSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str | None = None,
        type: str | None = None,
        host: str | None = None,
        key_name: str | None = None,
        event_hub_name: str | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
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
    def _load(cls: type[Self], resource: dict | str, cognite_client: CogniteClient = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsEventHubSource(**data, cognite_client=cognite_client)


class HostedExtractorsRestSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str | None = None,
        type: str | None = None,
        host: str | None = None,
        port: int | None = None,
        interval: str | None = None,
        pagination: dict[str, Any] | None = None,
        incremental_load: dict[str, Any] | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
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
    def _load(cls: type[Self], resource: dict | str, cognite_client: CogniteClient = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsRestSource(**data, cognite_client=cognite_client)


class HostedExtractorsKafkaSource(HostedExtractorsSource):
    def __init__(
        self,
        external_id: str | None = None,
        type: str | None = None,
        host: list[str] | None = None,
        use_tls: bool | None = None,
        username: str | None = None,
        password: str | None = None,
        ca_certificate: str | None = None,
        auth_certificate: str | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
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
    def _load(cls: type[Self], resource: dict | str, cognite_client: CogniteClient = None) -> Self:
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client)

        data = {to_snake_case(key): val for key, val in resource.items()}
        return HostedExtractorsKafkaSource(**data, cognite_client=cognite_client)


class HostedExtractorsJob(CogniteResource):
    def __init__(
        self,
        external_id: str | None = None,
        format: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        status: str | None = None,
        target_status: str | None = None,
        source_id: str | None = None,
        destination_id: str | None = None,
        created_time: int | None = None,
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
        external_id: str | None = None,
        session_id: int | None = None,
        created_time: int | None = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.session_id = session_id
        self.created_time = created_time
        self.cognite_client = cognite_client


class HostedExtractorsSourceList(CogniteResourceList):
    _RESOURCE = HostedExtractorsSource


class HostedExtractorsJobList(CogniteResourceList):
    _RESOURCE = HostedExtractorsJob


class HostedExtractorsDestinationList(CogniteResourceList):
    _RESOURCE = HostedExtractorsDestination
