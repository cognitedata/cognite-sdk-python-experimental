import importlib.util
import json as _json
import os
import sys
import time
from inspect import getsource
from numbers import Integral, Number
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Dict, List, Optional, Union
from zipfile import ZipFile

from cognite.client import CogniteClient, utils
from cognite.client._api_client import APIClient
from cognite.client.data_classes import TimestampRange
from cognite.client.exceptions import CogniteAPIError
from requests import Response

from cognite.experimental._api.transformation_schedules import TransformationSchedulesAPI
from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    OidcCredentials,
    Transformation,
    TransformationDestination,
    TransformationJobBlockade,
    TransformationList,
)
from cognite.experimental.data_classes.transformation_schedules import TransformationSchedule
from cognite.experimental.data_classes.transformations import TransformationFilter


class TransformationsAPI(APIClient):
    _RESOURCE_PATH = "/transformations"
    _LIST_CLASS = TransformationList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.jobs = TransformationJobsAPI(*args, **kwargs)
        self.schedules = TransformationSchedulesAPI(*args, **kwargs)
        # self.notifications = TransformationNotificationsAPI(*args, **kwargs)

    def create(
        self, transformation: Union[Transformation, List[Transformation]]
    ) -> Union[Transformation, TransformationList]:
        """`Create one or more transformations. <https://docs.cognite.com/api/playground/#operation/createTransformations>`_

        Args:
            transformation (Union[Transformation, List[Transformation]]) – Transformation or list of transformations to create.

        Returns:
            Created transformation(s)

        Examples:

            Create new transformations:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import Transfromation
                >>> c = CogniteClient()
                >>> transformations = [Transformation(name="transformation1"), Transformation(name="transformation2")]
                >>> res = c.transformations.create(transformations)
        """
        utils._auxiliary.assert_type(transformation, "transformation", [Transformation, list])
        return self._create_multiple(transformation)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        """`Delete one or more transformations. <https://docs.cognite.com/api/playground/#operation/deleteTransformations>`_

        Args:
            id (Union[int, List[int]): Id or list of ids.
            external_id (Union[str, List[str]]): External ID or list of external ids.

        Returns:
            None

        Example:

            Delete transformations by id or external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.transformations.delete(id=[1,2,3], external_id="function3")
        """
        self._delete_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def list(self, include_public: bool = True, limit: Optional[int] = LIST_LIMIT_DEFAULT,) -> TransformationList:
        """`List all transformations. <https://docs.cognite.com/api/playground/#operation/transformations>`_

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

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[Transformation]:
        """`Retrieve a single transformation by id. <https://docs.cognite.com/api/playground/#operation/getTransformation>`_

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID

        Returns:
            Optional[Transformation]: Requested transformation or None if it does not exist.

        Examples:

            Get transformation by id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.transformations.retrieve(id=1)

            Get transformation by external id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.transformations.retrieve(external_id="1")
        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

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
