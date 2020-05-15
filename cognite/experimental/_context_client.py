import functools
import re
from typing import Any, Dict, List, Union

from requests import Response

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import to_camel_case, to_snake_case
from cognite.experimental.data_classes import (
    ContextualizationJob,
    ContextualizationModel,
    ContextualizationModelList,
    EntityMatchingModel,
    ResourceTypingModel,
)


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

    def _run_job(self, job_path, status_path=None, headers=None, **kwargs) -> ContextualizationJob:
        if status_path is None:
            status_path = job_path + "/"
        return ContextualizationJob._load_with_status(
            self._camel_post(job_path, json=kwargs, headers=headers).json(),
            status_path=self._RESOURCE_PATH + status_path,
            cognite_client=self._cognite_client,
        )


class ContextModelAPI(ContextAPI):
    _MODEL_CLASS = ContextualizationModel

    def _fit_model(self, model_path="/fit", headers=None, **kwargs) -> Union[EntityMatchingModel, ResourceTypingModel]:
        response = self._camel_post(model_path, json=kwargs, headers=headers)
        return self._MODEL_CLASS._load(response.json(), cognite_client=self._cognite_client)

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
