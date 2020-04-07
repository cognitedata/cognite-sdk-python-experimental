import copy
import math
import time
from typing import Iterable, List, Union

from typing_extensions import TypedDict

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._auxiliary import to_camel_case
from cognite.experimental.exceptions import ModelFailedException


class ContextualizationJob(CogniteResource):
    def __init__(self, job_id=None, status=None, error_message=None, status_path=None, cognite_client=None, **kwargs):
        """Data class for the result of a contextualization job. All keys in the body become snake-cased variables in the class (e.g. `items`, `svg_url`)"""
        self.job_id = job_id
        self.status = status
        self.error_message = error_message
        self._cognite_client = cognite_client
        self._result = None

    def update_status(self) -> str:
        """Updates the model status and returns it"""
        data = self._cognite_client.entity_matching._get(f"{self.status_path}{self.job_id}").json()  # any playground
        self.status = data["status"]
        self.error_message = data.get("errorMessage")
        self._result = {k: v for k, v in data.items() if k not in {"status", "jobId", "errorMessage"}}
        return self.status

    def wait_for_completion(self, interval=1):
        """Waits for job completion, raising ModelFailedException if fit failed - generally not needed to call as it is called by result"""
        while True:
            self.update_status()
            if self.status not in ["Queued", "Running"]:
                break
            time.sleep(interval)
        if self.status == "Failed":
            raise ModelFailedException(self.__class__.__name__, self.job_id, self.error_message)

    @property
    def result(self):
        """Waits for the job to finish and returns the results."""
        if not self._result:
            self.wait_for_completion()
        return self._result

    def __str__(self):
        return "%s(id: %d,status: %s,error: %s)" % (
            self.__class__.__name__,
            self.job_id,
            self.status,
            self.error_message,
        )

    @staticmethod
    def _load_with_status(data, status_path, cognite_client):
        obj = ContextualizationJob._load(data, cognite_client=cognite_client)
        obj.status_path = status_path
        return obj


class ContextualizationModel(CogniteResource):
    """Abstract base class for contextualization models"""

    _STATUS_PATH = None

    def __init__(self, model_id=None, status=None, error_message=None, cognite_client=None):
        self.model_id = model_id
        self.status = status
        self.error_message = error_message
        self._cognite_client = cognite_client

    def __str__(self):
        return "%s(id: %d,status: %s,error: %s)" % (
            self.__class__.__name__,
            self.model_id,
            self.status,
            self.error_message,
        )

    def predict(self, asynchronous=False, **kwargs):
        raise NotImplementedError(f"Predict not implemented for {self.__class__}")

    def update_status(self) -> str:
        """Updates the model status and returns it"""
        data = self._cognite_client.entity_matching._get(f"{self._STATUS_PATH}{self.model_id}").json()
        self.status = data["status"]
        self.error_message = data.get("errorMessage")
        return self.status

    def wait_for_completion(self, interval=1):
        """Waits for model completion, raising ModelFailedException if fit failed - generally not needed to call as it is called by predict"""
        while True:
            self.update_status()
            if self.status not in ["Queued", "Running"]:
                break
            time.sleep(interval)
        if self.status == "Failed":
            raise ModelFailedException(self.__class__.__name__, self.model_id, self.error_message)


class EntityMatchingModel(ContextualizationModel):
    _RESOURCE_PATH = "/context/entity_matching"
    _STATUS_PATH = _RESOURCE_PATH + "/"

    def predict(self, entities: Iterable[str]) -> ContextualizationJob:
        """Predict entity matching.

        Args:
            items (Iterable[str]): entities (e.g. time series) to predict matching entity of (e.g. asset)

        Returns:
            ContextualizationJob: object which can be used to wait for and retrieve results."""
        self.wait_for_completion()
        return self._cognite_client.entity_matching._run_job(job_path=f"/{self.model_id}/predict", items=list(entities))


class TypingPredictData(TypedDict):
    data: List[str]


class TypingFitData(TypedDict):
    data: List[str]
    target: str


class ResourceTypingModel(ContextualizationModel):
    _RESOURCE_PATH = "/context/resource_typing"
    _STATUS_PATH = _RESOURCE_PATH + "/"

    @staticmethod
    def format_items(
        items: List[Union[TypingFitData, TypingPredictData]]
    ) -> List[Union[TypingFitData, TypingPredictData]]:
        items = copy.deepcopy(items)
        for item in items:
            item["data"] = ["" if isinstance(x, float) and math.isnan(x) else x for x in item["data"]]
        return items

    def predict(self, items: Iterable[TypingPredictData]) -> ContextualizationJob:
        """Predict resource types

        Args:
            items (Iterable[TypingPredictData]): entities to predict type of, in the same for as passed to fit.

        Returns:
            ContextualizationJob: object which can be used to wait for and retrieve results."""
        self.wait_for_completion()
        return self._cognite_client.resource_typing._run_job(
            job_path=f"/{self.model_id}/predict", items=self.format_items(items)
        )


class ContextualizationModelList(CogniteResourceList):
    _RESOURCE = ContextualizationModel
    _ASSERT_CLASSES = False
