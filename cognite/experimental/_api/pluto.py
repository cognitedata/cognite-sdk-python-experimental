from typing import List, Optional, Union

from cognite.client import ClientConfig
from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type
from cognite.client.utils._identifier import IdentifierSequence

from cognite.experimental.data_classes.pluto import (
    PlutoDestination,
    PlutoDestinationList,
    PlutoJob,
    PlutoJobList,
    PlutoSource,
    PlutoSourceList,
)


class PlutoAPI(APIClient):
    _RESOURCE_PATH = "/pluto"

    def __init__(self, config: ClientConfig, api_version: Optional[str], cognite_client: "CogniteClient") -> None:
        super().__init__(config, api_version, cognite_client)
        self.sources = PlutoSourcesAPI(config, api_version, cognite_client)
        self.jobs = PlutoJobsAPI(config, api_version, cognite_client)
        self.destinations = PlutoDestinationsAPI(config, api_version, cognite_client)


class PlutoJobsAPI(APIClient):
    _RESOURCE_PATH = "/pluto/jobs"

    def __init__(self, config: ClientConfig, api_version: Optional[str], cognite_client: "CogniteClient") -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: Optional[str] = None, destination_external_id: Optional[str] = None, limit: int = 10
    ) -> PlutoJobList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=PlutoJobList,
            resource_cls=PlutoJob,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "alpha"},
        )

    def create(self, jobs: Union[PlutoJob, List[PlutoJob]]) -> Union[PlutoJob, List[PlutoJob]]:
        assert_type(jobs, "jobs", [PlutoJob, list])
        return self._create_multiple(
            items=jobs, list_cls=PlutoJobList, resource_cls=PlutoJob, headers={"cdf-version": "alpha"}
        )

    def delete(self, external_id: Union[str, List[str]]) -> None:
        self._delete_multiple(
            resource_path="/pluto/jobs",
            identifiers=IdentifierSequence.load(external_ids=external_id),
            wrap_ids=True,
            headers={"cdf-version": "alpha"},
        )


class PlutoSourcesAPI(APIClient):
    _RESOURCE_PATH = "/pluto/sources"

    def __init__(self, config: ClientConfig, api_version: Optional[str], cognite_client: "CogniteClient") -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: Optional[str] = None, destination_external_id: Optional[str] = None, limit: int = 10
    ) -> PlutoSourceList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=PlutoSourceList,
            resource_cls=PlutoSource,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "alpha"},
        )

    def create(self, jobs: Union[PlutoSource, List[PlutoSource]]) -> Union[PlutoSource, List[PlutoSource]]:
        assert_type(jobs, "jobs", [PlutoSource, list])
        return self._create_multiple(
            items=jobs, list_cls=PlutoSourceList, resource_cls=PlutoSource, headers={"cdf-version": "alpha"}
        )

    def delete(self, external_id: Union[str, List[str]]) -> None:
        self._delete_multiple(
            identifiers=IdentifierSequence.load(external_ids=external_id),
            wrap_ids=True,
            headers={"cdf-version": "alpha"},
        )


class PlutoDestinationsAPI(APIClient):
    _RESOURCE_PATH = "/pluto/destinations"

    def __init__(self, config: ClientConfig, api_version: Optional[str], cognite_client: "CogniteClient") -> None:
        super().__init__(config, api_version, cognite_client)

    def list(
        self, source_external_id: Optional[str] = None, destination_external_id: Optional[str] = None, limit: int = 10
    ) -> PlutoDestinationList:
        filter = {}
        if source_external_id:
            filter["source_external_id"] = source_external_id
        if destination_external_id:
            filter["destination_external_id"] = destination_external_id
        return self._list(
            list_cls=PlutoDestinationList,
            resource_cls=PlutoDestination,
            method="GET",
            limit=limit,
            filter=filter,
            headers={"cdf-version": "alpha"},
        )

    def create(
        self, jobs: Union[PlutoDestination, List[PlutoDestination]]
    ) -> Union[PlutoDestination, List[PlutoDestination]]:
        assert_type(jobs, "jobs", [PlutoDestination, list])
        return self._create_multiple(
            items=jobs, list_cls=PlutoDestinationList, resource_cls=PlutoDestination, headers={"cdf-version": "alpha"}
        )

    def delete(self, external_id: Union[str, List[str]]) -> None:
        self._delete_multiple(
            identifiers=IdentifierSequence.load(external_ids=external_id),
            wrap_ids=True,
            headers={"cdf-version": "alpha"},
        )
