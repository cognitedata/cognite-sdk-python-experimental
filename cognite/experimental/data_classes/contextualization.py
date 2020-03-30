import copy
import math
from typing import *
from typing import Iterable, List, Union

from typing_extensions import TypedDict

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class ContextualizationModel(CogniteResource):
    def __init__(self, model_id=None, status=None, error_message=None, cognite_client=None):
        self.model_id = model_id
        self.status = status
        self.error_message = error_message
        self._cognite_client = cognite_client

    def __str__(self):
        if self.error_message:
            return "ContextualizationModel(id: %d,status: %s,error: %s)" % (
                self.model_id,
                self.status,
                self.error_message,
            )
        else:
            return "ContextualizationModel(id: %d,status: %s)" % (self.model_id, self.status)

    def predict(self, asynchronous=False, **kwargs):
        raise NotImplementedError(f"Predict not implemented for {self.__class__}")


class ContextualizationJob(CogniteResource):
    def __init__(self, job_id=None, status=None, error_message=None, cognite_client=None, **kwargs):
        """Data class for the result of a contextualization job. All keys in the body become snake-cased variables in the class (e.g. `items`, `svg_url`)"""
        self.job_id = job_id
        self.status = status
        self.error_message = error_message
        self._cognite_client = cognite_client
        self.result_keys = list(kwargs.keys())
        for k, v in (kwargs or {}).items():
            setattr(self, k, v)

    def __str__(self):
        if self.error_message:
            return "ContextualizationJob(id: %d, status: %s, error: %s)" % (
                self.job_id,
                self.status,
                self.error_message,
            )
        elif self.result_keys:
            return "ContextualizationJob(id: %d, status: %s, results: %s)" % (
                self.job_id,
                self.status,
                self.result_keys,
            )
        else:
            return "ContextualizationJob(id: %d, status: %s)" % (self.job_id, self.status)


class ContextualizationModelList(CogniteResourceList):
    _RESOURCE = ContextualizationModel
    _ASSERT_CLASSES = False


class EntityMatchingModel(ContextualizationModel):
    def predict(self, entities: Iterable[str]) -> "Task[ContextualizationJob]":
        """Predict entity matching

        Args:
            items (Iterable[str]): entities (e.g. time series) to predict matching entity of (e.g. asset)

        Returns:
            Task[ContextualizationJob]: Task which waits for the job to be completed."""
        return self._cognite_client.entity_matching._run_job(
            job_path=f"/{self.model_id}/predict", status_path=f"/{self.model_id}/predict/", items=list(entities)
        )


class TypingPredictData(TypedDict):
    data: List[str]


class TypingFitData(TypedDict):
    data: List[str]
    target: str


class ResourceTypingModel(ContextualizationModel):
    @staticmethod
    def format_items(
        items: List[Union[TypingFitData, TypingPredictData]]
    ) -> List[Union[TypingFitData, TypingPredictData]]:
        items = copy.deepcopy(items)
        for item in items:
            item["data"] = ["" if isinstance(x, float) and math.isnan(x) else x for x in item["data"]]
        return items

    def predict(self, items: Iterable[TypingPredictData]) -> "Task[ContextualizationJob]":
        """Predict resource types

        Args:
            items (Iterable[TypingPredictData]): entities to predict type of, in the same for as passed to fit.

        Returns:
            Task[ContextualizationJob]: Task which waits for the job to be completed."""
        return self._cognite_client.resource_typing._run_job(
            job_path=f"/{self.model_id}/predict",
            status_path=f"/{self.model_id}/predict/",
            items=self.format_items(items),
        )
