import copy
import math
import time
from typing import Dict, Iterable, List, Optional, Tuple, Union

from typing_extensions import TypedDict

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.utils._auxiliary import to_camel_case
from cognite.experimental.exceptions import ModelFailedException


class ContextualizationJob(CogniteResource):
    def __init__(
        self,
        job_id=None,
        status=None,
        error_message=None,
        request_timestamp=None,
        start_timestamp=None,
        status_timestamp=None,
        status_path=None,
        cognite_client=None,
        **kwargs,
    ):
        """Data class for the result of a contextualization job. All keys in the body become snake-cased variables in the class (e.g. `items`, `svg_url`)"""
        self.job_id = job_id
        self.status = status
        self.request_timestamp = request_timestamp
        self.start_timestamp = start_timestamp
        self.status_timestamp = status_timestamp
        self.error_message = error_message
        self._cognite_client = cognite_client
        self._result = None
        self._status_path = status_path

    def update_status(self) -> str:
        """Updates the model status and returns it"""
        data = self._cognite_client.entity_matching._get(f"{self._status_path}{self.job_id}").json()  # any playground
        self.status = data["status"]
        self.status_timestamp = data.get("statusTimestamp")
        self.start_timestamp = data.get("startTimestamp")
        self.request_timestamp = self.request_timestamp or data.get("requestTimestamp")
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
        obj._status_path = status_path
        return obj


class ContextualizationModel(CogniteResource):
    """Abstract base class for contextualization models"""

    _STATUS_PATH = None

    def __init__(
        self,
        model_id=None,
        status=None,
        error_message=None,
        request_timestamp=None,
        start_timestamp=None,
        status_timestamp=None,
        cognite_client=None,
    ):
        self.model_id = model_id
        self.status = status
        self.request_timestamp = request_timestamp
        self.start_timestamp = start_timestamp
        self.status_timestamp = status_timestamp
        self.error_message = error_message
        self._cognite_client = cognite_client

    def __str__(self):
        return "%s(id: %d,status: %s,error: %s)" % (
            self.__class__.__name__,
            self.model_id,
            self.status,
            self.error_message,
        )

    def update_status(self) -> str:
        """Updates the model status and returns it"""
        data = self._cognite_client.entity_matching._get(f"{self._STATUS_PATH}{self.model_id}").json()
        self.status = data["status"]
        self.status_timestamp = data.get("statusTimestamp")
        self.start_timestamp = data.get("startTimestamp")
        self.request_timestamp = self.request_timestamp or data.get("requestTimestamp")
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
    def __init__(
        self,
        model_id=None,
        status=None,
        error_message=None,
        request_timestamp=None,
        start_timestamp=None,
        status_timestamp=None,
        cognite_client=None,
        classifier=None,
        feature_type=None,
        keys_from_to=None,
        model_type=None,
    ):
        super().__init__(
            model_id, status, error_message, request_timestamp, start_timestamp, status_timestamp, cognite_client
        )
        self.classifier = classifier
        self.feature_type = feature_type
        self.keys_from_to = keys_from_to
        self.model_type = model_type

    _RESOURCE_PATH = "/context/entity_matching"
    _STATUS_PATH = _RESOURCE_PATH + "/"

    def predict(
        self,
        match_from: Optional[List[Dict]] = None,
        match_to: Optional[List[Dict]] = None,
        num_matches=1,
        score_threshold=None,
        complete_missing=False,
    ) -> ContextualizationJob:
        """Predict entity matching.

        Args:
            match_from: entities to match from, does not need an 'id' field. Tolerant to passing more than is needed or used (e.g. json dump of time series list). If omitted, will use data from fit.
            match_to: entities to match to, does not need an 'id' field.  Tolerant to passing more than is needed or used. If omitted, will use data from fit.
            num_matches (int): number of matches to return for each item.
            score_threshold (float): only return matches with a score above this threshold
            complete_missing (bool): whether missing data in keyFrom or keyTo should be filled in with an empty string.

        Returns:
            ContextualizationJob: object which can be used to wait for and retrieve results."""
        self.wait_for_completion()
        return self._cognite_client.entity_matching._run_job(
            job_path=f"/{self.model_id}/predict",
            match_from=self.dump_entities(match_from),
            match_to=self.dump_entities(match_to),
            num_matches=num_matches,
            score_threshold=score_threshold,
            complete_missing=complete_missing,
        )

    def predict_ml(
        self,
        match_from: Optional[List[Dict]] = None,
        match_to: Optional[List[Dict]] = None,
        num_matches=1,
        score_threshold=None,
        complete_missing=False,
    ) -> ContextualizationJob:
        """Duplicate of predict will eventually be removed"""
        self.wait_for_completion()
        return self._cognite_client.entity_matching._run_job(
            job_path=f"/{self.model_id}/predict",
            match_from=self.dump_entities(match_from),
            match_to=self.dump_entities(match_to),
            num_matches=num_matches,
            score_threshold=score_threshold,
            complete_missing=complete_missing,
        )

    def refit(self, true_matches: List[Tuple[int, int]]) -> "EntityMatchingModel":
        """Re-fits an entity matching on updated data.

        Args:
            true_matches: Updated known valid matches given as a list of (id_from,id_to).
        Returns:
            EntityMatchingModel: new model refitted to ."""
        self.wait_for_completion()
        return self._cognite_client.entity_matching._fit_model(
            model_path=f"/{self.model_id}/refit", true_matches=true_matches
        )

    @staticmethod
    def dump_entities(entities: List[Union[Dict, CogniteResource]]) -> Optional[List[Dict]]:
        if entities:
            return [
                {k: v for k, v in e.dump(camel_case=True).items() if isinstance(v, str) or k == "id"}
                if isinstance(e, CogniteResource)
                else e
                for e in entities
            ]


class ContextualizationModelList(CogniteResourceList):
    _RESOURCE = ContextualizationModel
    _ASSERT_CLASSES = False
