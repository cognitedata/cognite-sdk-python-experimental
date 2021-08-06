import json as _json
from typing import List, Optional, Union

from cognite.client import CogniteClient, utils
from cognite.client._api_client import APIClient
from requests import Response

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    OidcCredentials,
    Transformation,
    TransformationDestination,
    TransformationJobBlockade,
    TransformationList,
    TransformationSchedule,
    TransformationScheduleList,
)
from cognite.experimental.data_classes.transformations import TransformationFilter


class TransformationSchedulesAPI(APIClient):
    _RESOURCE_PATH = "/transformations/schedules"
    _LIST_CLASS = TransformationScheduleList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self, schedule: Union[TransformationSchedule, List[TransformationSchedule]]
    ) -> Union[TransformationSchedule, TransformationScheduleList]:
        """`Schedule the specified transformation with the specified configuration(s). <https://docs.cognite.com/api/playground/#operation/scheduleTransformations>`_

        Args:
            schedule (Union[TransformationSchedule, List[TransformationSchedule]]) – Configuration or list of configurations of the schedules to create.

        Returns:
            Created schedule(s)

        Examples:

            Create new schedules:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import Transfromation
                >>> c = CogniteClient()
                >>> schedules = [TransformationSchedule(name="transformation1"), TransformationSchedule(name="transformation2")]
                >>> res = c.transformations.schedule(schedules)
        """
        utils._auxiliary.assert_type(schedule, "schedule", [TransformationSchedule, list])
        return self._create_multiple(schedule)

    def list(self, include_public: bool = True, limit: Optional[int] = LIST_LIMIT_DEFAULT,) -> TransformationList:
        """`List all transformation schedules. <https://docs.cognite.com/api/playground/#operation/transformationSchedules>`_

        Args:
            include_public (bool): Whether public transformations should be included in the results. (default true).
            cursor (str): Cursor for paging through results.
            limit (int): Limits the number of results to be returned. The maximum is 1000, default limit is 25.

        Returns:
            TransformationList: List of transformations

        Example:

            List transformations::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> transformations_list = c.transformations.list()
        """
        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        filter = TransformationFilter(include_public=include_public).dump(camel_case=True)

        return self._list(method="GET", limit=limit, filter=filter,)

    def delete(
        self,
        id: Union[int, List[int]] = None,
        external_id: Union[str, List[str]] = None,
        ignore_unknown_ids: bool = False,
    ) -> None:
        """`Unsubscribe one or more schedules <https://doc.cognitedata.com/api/playground/#operation/deleteSchedules>`_

        Args:
            id (Union[int, List[int]): Id or list of ids
            external_id (Union[str, List[str]]): External ID or list of exgernal ids
            ignore_unknown_ids (bool): Ignore IDs and external IDs that are not found rather than throw an exception.

        Returns:
            None

        Examples:

            Delete schedules by id or external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.transformations.schedules.delete(id=[1,2,3], external_id="3")
        """
        self._delete_multiple(
            ids=id, external_ids=external_id, wrap_ids=True, extra_body_fields={"ignoreUnknownIds": ignore_unknown_ids},
        )

    def _do_request(self, method: str, url_path: str, **kwargs) -> Response:
        is_retryable, full_url = self._resolve_url(method, url_path)

        json_payload = kwargs.get("json")
        headers = self._configure_headers(self._config.headers.copy())
        headers.update(kwargs.get("headers") or {})

        if json_payload:
            data = _json.dumps(json_payload, default=utils._auxiliary.json_dump_default)
            kwargs["data"] = data

        kwargs["headers"] = headers

        # requests will by default follow redirects. This can be an SSRF-hazard if
        # the client can be tricked to request something with an open redirect, in
        # addition to leaking the token, as requests will send the headers to the
        # redirected-to endpoint.
        # If redirects are to be followed in a call, this should be opted into instead.
        kwargs.setdefault("allow_redirects", False)

        if is_retryable:
            res = self._http_client_with_retry.request(method=method, url=full_url, **kwargs)
        else:
            res = self._http_client.request(method=method, url=full_url, **kwargs)

        if not self._status_ok(res.status_code):
            self._raise_API_error(res, payload=json_payload)
        self._log_request(res, payload=json_payload)
        return res
