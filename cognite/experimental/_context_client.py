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

    def _fit_model(self, model_path="/fit", headers=None, **kwargs) -> EntityMatchingModel:
        response = self._camel_post(model_path, json=kwargs, headers=headers)
        return self._MODEL_CLASS._load(response.json(), cognite_client=self._cognite_client)

    def retrieve(self, model_id: int) -> EntityMatchingModel:
        """Retrieve model status

        Args:
            model_id: id of the model to retrieve.

        Returns:
            ContextualizationModel: Model requested."""
        return self._MODEL_CLASS._load(self._camel_get(f"/{model_id}").json(), cognite_client=self._cognite_client)

    def list(self, filter: Dict = None) -> ContextualizationModelList:
        """List models

        Args:
            filter (dict): If not None, return models with parameter values that matches what is specified in the filter.

        Returns:
            ContextualizationModelList: List of models."""
        filter = {to_camel_case(k): v for k, v in (filter or {}).items() if v is not None}
        models = self._camel_post("/list", json={"filter": filter}).json()["items"]
        return ContextualizationModelList(
            [self._MODEL_CLASS._load(model, cognite_client=self._cognite_client) for model in models]
        )

    def list_jobs(self) -> ContextualizationModelList:
        """List jobs

        Returns:
            ContextualizationModelList: List of jobs."""
        return ContextualizationModelList(
            [
                self._MODEL_CLASS._load(model, cognite_client=self._cognite_client)
                for model in self._camel_get("/jobs").json()["items"]
            ]
        )

    def update(self, model: EntityMatchingModel) -> ContextualizationModelList:
        """ Update model

        Args:
            model (ContextualizationModel) : Model to update
        """
        model_attributes = self.retrieve(model_id=model.model_id).__dict__
        model_update_attributes = model.__dict__
        # Find the attributes/parameters that differs and should be updated
        attributes_update = [
            key
            for key in model_attributes.keys()
            if model_attributes[key] != model_update_attributes[key]
            and key not in ContextualizationModel().__dict__.keys()
        ]
        update_dict = {}
        for attribute in attributes_update:
            update_dict[attribute] = {"set": model_update_attributes[attribute]}

        response = self._camel_post("/update", json={"items": [{"modelId": model.model_id, "update": update_dict}]})
        return ContextualizationModelList([self.retrieve(model_id=model.model_id)])

    def delete(self, model_id: Union[List, ContextualizationModelList, int, ContextualizationModel]) -> None:
        """Delete models

        Args:
             model_id (Union[list, ContextualizationModelList, int, ContextualizationModel): model or list of models to delete."""
        if not isinstance(model_id, (list, ContextualizationModelList)):
            model_id = [model_id]
        model_id = [m.model_id if isinstance(m, ContextualizationModel) else m for m in model_id]
        self._camel_post("/delete", {"items": [{"id": id} for id in model_id]})
