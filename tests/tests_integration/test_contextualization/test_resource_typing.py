import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, ResourceTypingModel

COGNITE_CLIENT = CogniteClient()
RTAPI = COGNITE_CLIENT.resource_typing


class TestResourceTypingIntegration:
    def test_fit(self):
        items = [{"data": ["a", "b'"], "target": "x"}, {"data": ["c", "d'"], "target": "y"}] * 2
        targets_to_classify = ["x"]

        model = RTAPI.fit(items, targets_to_classify=targets_to_classify)
        assert isinstance(model, ResourceTypingModel)
        assert "Queued" == model.status
        job = model.predict(items=[{"data": ["a", "b'"]}])
        assert "Completed" == model.status
        assert isinstance(job, ContextualizationJob)
        assert isinstance(job.result["items"], list)
        assert {"data", "score", "target"} == job.result["items"][0].keys()
        RTAPI.delete(model)
