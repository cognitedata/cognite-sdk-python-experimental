import copy
import math
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
    def __init__(self, job_id=None, status=None, error_message=None, items=None, cognite_client=None, **kwargs):
        self.job_id = job_id
        self.status = status
        self.error_message = error_message
        self._cognite_client = cognite_client
        self.result = items
        if kwargs:
            self.args = kwargs

    def __str__(self):
        if self.error_message:
            return "ContextualizationJob(id: %d, status: %s, error: %s)" % (
                self.job_id,
                self.status,
                self.error_message,
            )
        elif self.result:
            return "ContextualizationJob(id: %d, status: %s, result: available)" % (self.job_id, self.status)
        else:
            return "ContextualizationJob(id: %d, status: %s)" % (self.job_id, self.status)


class ContextualizationModelList(CogniteResourceList):
    _RESOURCE = ContextualizationModel
    _ASSERT_CLASSES = False


class EntityMatchingModel(ContextualizationModel):
    def predict(self, entities: Iterable[str]) -> "Task[ContextualizationJob]":
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
        return self._cognite_client.resource_typing._run_job(
            job_path=f"/{self.model_id}/predict",
            status_path=f"/{self.model_id}/predict/",
            items=self.format_items(items),
        )
