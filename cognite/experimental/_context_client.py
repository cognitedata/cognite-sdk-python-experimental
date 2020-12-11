import functools
import re
from typing import Any, Dict, List, Union

from cognite.client._api_client import APIClient
from cognite.client.data_classes import ContextualizationJob
from cognite.client.utils._auxiliary import to_camel_case, to_snake_case
from requests import Response


class ContextAPI(APIClient):
    def _camel_post(
        self,
        context_path: str,
        json: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        headers: Dict[str, Any] = None,
    ) -> Response:
        return self._post(
            self._RESOURCE_PATH + context_path,
            json={to_camel_case(k): v for k, v in (json or {}).items() if v is not None},
            params=params,
            headers=headers,
        )

    def _camel_get(self, context_path: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Response:
        return self._get(
            self._RESOURCE_PATH + context_path,
            params={to_camel_case(k): v for k, v in (params or {}).items() if v is not None},
            headers=headers,
        )

    def _run_job(self, job_path, status_path=None, headers=None, job_cls=None, **kwargs) -> ContextualizationJob:
        job_cls = job_cls or ContextualizationJob
        if status_path is None:
            status_path = job_path + "/"
        return job_cls._load_with_status(
            self._camel_post(job_path, json=kwargs, headers=headers).json(),
            status_path=self._RESOURCE_PATH + status_path,
            cognite_client=self._cognite_client,
        )
