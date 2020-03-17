import asyncio

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


class TestEntityMatchingIntegration:
    @pytest.mark.asyncio
    async def test_fit(self):
        entities = ["a-1", "b-2"]
        resp = EMAPI.fit(entities)
        assert isinstance(resp, asyncio.Task)
        model = await resp
        assert isinstance(model, EntityMatchingModel)
        assert "Completed" == model.status

        jobtask = model.predict("a1")
        assert isinstance(jobtask, asyncio.Task)
        job = await jobtask
        assert isinstance(job, ContextualizationJob)
        assert {"input", "predicted", "score"} == set(job.items[0].keys())
        EMAPI.delete(model)
