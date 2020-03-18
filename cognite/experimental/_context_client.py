import asyncio
import functools
import re
from typing import Any, Dict, List, Union

from requests import Response

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import to_camel_case, to_snake_case
from cognite.experimental.data_classes import ContextualizationJob, ContextualizationModel, ContextualizationModelList
from cognite.experimental.exceptions import ModelFailedException


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

    async def _wait_for_result(self, response, status_path="/", type="job", interval=1) -> Dict:
        data = response.json()
        id = data[type + "Id"]
        while True:
            data = self._camel_get(f"{status_path}{id}").json()
            if data["status"] == "Failed":
                raise ModelFailedException(type, id, data.get("errorMessage"))
            if data["status"] == "Completed":
                break
            await asyncio.sleep(interval)
        return data

    async def _wait_for_job_result(self, response, status_path="/", interval=1) -> ContextualizationJob:
        json = await self._wait_for_result(response, status_path, "job", interval)
        return ContextualizationJob(cognite_client=self, **{to_snake_case(k): v for k, v in json.items()})

    def _run_job(self, job_path, status_path="/", headers=None, **kwargs) -> "asyncio.Task[ContextualizationJob]":
        response = self._camel_post(job_path, json=kwargs, headers=headers)
        return asyncio.get_event_loop().create_task(self._wait_for_job_result(response, status_path))


class ContextModelAPI(ContextAPI):
    _MODEL_CLASS = ContextualizationModel

    async def _wait_for_model_result(self, response, status_path="/", interval=1) -> ContextualizationModel:
        return self._MODEL_CLASS._load(
            await self._wait_for_result(response, status_path, "model", interval), cognite_client=self._cognite_client
        )

    def _fit_model(
        self, model_path="/fit", status_path="/", headers=None, **kwargs
    ) -> "asyncio.Task[ContextualizationModel]":
        response = self._camel_post(model_path, json=kwargs, headers=headers)
        return asyncio.get_event_loop().create_task(self._wait_for_model_result(response, status_path))  # 3.6 compat

    def retrieve(self, model_id: int) -> ContextualizationModel:
        """Retrieve model status

        Args:
            model_id: id of the model to retrieve.

        Returns:
            ContextualizationModel: Model requested."""
        return self._MODEL_CLASS._load(self._camel_get(f"/{model_id}").json(), cognite_client=self._cognite_client)

    def list(self) -> ContextualizationModelList:
        """List models

        Returns:
            ContextualizationModelList: List of models."""
        return ContextualizationModelList(
            [
                self._MODEL_CLASS._load(model, cognite_client=self._cognite_client)
                for model in self._camel_get("/").json()["items"]
            ]
        )

    def delete(self, model_id: Union[List, ContextualizationModelList, int, ContextualizationModel]) -> None:
        """Delete models

        Args:
             model_id (Union[list, ContextualizationModelList, int, ContextualizationModel): model or list of models to delete."""
        if not isinstance(model_id, (list, ContextualizationModelList)):
            model_id = [model_id]
        model_id = [m.model_id if isinstance(m, ContextualizationModel) else m for m in model_id]
        self._camel_post("/delete", {"items": [{"modelId": id} for id in model_id]})
