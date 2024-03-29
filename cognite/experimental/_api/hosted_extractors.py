from __future__ import annotations

from typing import TYPE_CHECKING

from cognite.client import ClientConfig
from cognite.client._api_client import APIClient
from cognite.client.utils._identifier import IdentifierSequence
from cognite.client.utils._validation import assert_type
from cognite.experimental.data_classes.hosted_extractors import (
    HostedExtractorsDestination,
    HostedExtractorsDestinationList,
    HostedExtractorsJob,
    HostedExtractorsJobList,
    HostedExtractorsSource,
    HostedExtractorsSourceList,
)

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class HostedExtractorsAPI(APIClient):
    _RESOURCE_PATH = "/hostedextractors"

    def __init__(self, config: ClientConfig, api_version: str | None, cognite_client: CogniteClient) -> None:
        super().__init__(config, api_version, cognite_client)
        self.sources = HostedExtractorsSourcesAPI(config, api_version, cognite_client)
        self.jobs = HostedExtractorsJobsAPI(config, api_version, cognite_client)
        self.destinations = HostedExtractorsDestinationsAPI(config, api_version, cognite_client)


class HostedExtractorsJobsAPI(APIClient):
    _RESOURCE_PATH = "/hostedextractors/jobs"

    def __init__(self, config: ClientConfig, api_version: str | None, cognite_client: CogniteClient) -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: str | None = None, destination_external_id: str | None = None, limit: int = 10
    ) -> HostedExtractorsJobList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=HostedExtractorsJobList,
            resource_cls=HostedExtractorsJob,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "beta"},
        )

    def create(
        self, jobs: HostedExtractorsJob | list[HostedExtractorsJob]
    ) -> HostedExtractorsJob | list[HostedExtractorsJob]:
        assert_type(jobs, "jobs", [HostedExtractorsJob, list])
        return self._create_multiple(
            items=jobs,
            list_cls=HostedExtractorsJobList,
            resource_cls=HostedExtractorsJob,
            headers={"cdf-version": "beta"},
        )

    def delete(self, external_id: str | list[str]) -> None:
        self._delete_multiple(
            resource_path="/hostedextractors/jobs",
            identifiers=IdentifierSequence.load(external_ids=external_id),
            wrap_ids=True,
            headers={"cdf-version": "beta"},
        )


class HostedExtractorsSourcesAPI(APIClient):
    _RESOURCE_PATH = "/hostedextractors/sources"

    def __init__(self, config: ClientConfig, api_version: str | None, cognite_client: CogniteClient) -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: str | None = None, destination_external_id: str | None = None, limit: int = 10
    ) -> HostedExtractorsSourceList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=HostedExtractorsSourceList,
            resource_cls=HostedExtractorsSource,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "beta"},
        )

    def create(
        self, sources: HostedExtractorsSource | list[HostedExtractorsSource]
    ) -> HostedExtractorsSource | list[HostedExtractorsSource]:
        assert_type(sources, "sources", [HostedExtractorsSource, list])
        return self._create_multiple(
            items=sources,
            list_cls=HostedExtractorsSourceList,
            resource_cls=HostedExtractorsSource,
            headers={"cdf-version": "beta"},
        )

    def delete(
        self, external_id: str | list[str], force: bool | None = None, ignore_unknown_ids: bool | None = None
    ) -> None:
        extras = {}
        if force is not None:
            extras["force"] = force
        if ignore_unknown_ids is not None:
            extras["ignoreUnknownIds"] = ignore_unknown_ids

        self._delete_multiple(
            identifiers=IdentifierSequence.load(external_ids=external_id),
            wrap_ids=True,
            extra_body_fields=extras if extras else None,
            headers={"cdf-version": "beta"},
        )


class HostedExtractorsDestinationsAPI(APIClient):
    _RESOURCE_PATH = "/hostedextractors/destinations"

    def __init__(self, config: ClientConfig, api_version: str | None, cognite_client: CogniteClient) -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: str | None = None, destination_external_id: str | None = None, limit: int = 10
    ) -> HostedExtractorsDestinationList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=HostedExtractorsDestinationList,
            resource_cls=HostedExtractorsDestination,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "beta"},
        )

    def create(
        self, destinations: HostedExtractorsDestination | list[HostedExtractorsDestination]
    ) -> HostedExtractorsDestination | list[HostedExtractorsDestination]:
        assert_type(destinations, "destinations", [HostedExtractorsDestination, list])
        return self._create_multiple(
            items=destinations,
            list_cls=HostedExtractorsDestinationList,
            resource_cls=HostedExtractorsDestination,
            headers={"cdf-version": "beta"},
        )

    def delete(
        self, external_id: str | list[str], force: bool | None = None, ignore_unknown_ids: bool | None = None
    ) -> None:
        extras = {}
        if force is not None:
            extras["force"] = force
        if ignore_unknown_ids is not None:
            extras["ignoreUnknownIds"] = ignore_unknown_ids

        self._delete_multiple(
            identifiers=IdentifierSequence.load(external_ids=external_id),
            extra_body_fields=extras if extras else None,
            wrap_ids=True,
            headers={"cdf-version": "beta"},
        )
