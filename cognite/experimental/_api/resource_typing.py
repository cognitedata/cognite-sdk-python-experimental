from typing import List

from cognite.experimental._context_client import ContextModelAPI
from cognite.experimental.data_classes import ContextualizationJob, ResourceTypingModel, TypingFitData


class ResourceTypingAPI(ContextModelAPI):
    _RESOURCE_PATH = "/context/resource_typing"
    _MODEL_CLASS = ResourceTypingModel

    def fit(
        self,
        items: List[TypingFitData],
        algorithm: str = "open_set_nearest_neighbors",
        targets_to_classify: List[str] = None,
    ) -> "Task[ContextualizationModel]":
        return self._fit_model(
            items=ResourceTypingModel.format_items(items), algorithm=algorithm, targets_to_classify=targets_to_classify
        )
