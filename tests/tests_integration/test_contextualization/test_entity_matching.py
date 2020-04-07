import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


class TestEntityMatchingIntegration:
    def test_fit(self):
        entities = ["a-1", "b-2"]
        model = EMAPI.fit(entities)
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status

        job = model.predict("a1")
        assert "Completed" == model.status
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"input", "predicted", "score"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status
        EMAPI.delete(model)
