from typing import List

from cognite.experimental._context_client import ContextModelAPI
from cognite.experimental.data_classes import ContextualizationJob, ResourceTypingModel, TypingFitData


class ResourceTypingAPI(ContextModelAPI):
    _RESOURCE_PATH = ResourceTypingModel._RESOURCE_PATH
    _MODEL_CLASS = ResourceTypingModel

    def fit(
        self,
        items: List[TypingFitData],
        algorithm: str = "open_set_nearest_neighbors",
        targets_to_classify: List[str] = None,
    ) -> ResourceTypingModel:
        """Fit entity matching model.

        Args:
            items (List[TypingFitData]): List of entities (e.g. asset name and description) and corresponding type.
            algorithm (str): The type of model to use for classification, either "open_set_nearest_neighbors" "deep_open_classifier"
            targets_to_classify (str): The classes the model will try to classify items into. All other targets will be treated as a single 'other' class.

        Returns:
            ResourceTypingModel: Resulting queued model."""
        return self._fit_model(
            items=ResourceTypingModel.format_items(items), algorithm=algorithm, targets_to_classify=targets_to_classify
        )
