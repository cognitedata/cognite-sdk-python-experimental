import asyncio

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, ResourceTypingModel

COGNITE_CLIENT = CogniteClient()
RTAPI = COGNITE_CLIENT.resource_typing


class TestResourceTypingIntegration:
    @pytest.mark.asyncio
    async def test_fit(self):
        items = [{"data": ["a", "b'"], "target": "x"}, {"data": ["c", "d'"], "target": "y"}] * 2
        targets_to_classify = ["x"]

        resp = RTAPI.fit(items, targets_to_classify=targets_to_classify)
        assert isinstance(resp, asyncio.Task)
        model = await resp
        assert isinstance(model, ResourceTypingModel)
        assert "Completed" == model.status
        jt = model.predict(items=[{"data": ["a", "b'"]}])
        assert isinstance(jt, asyncio.Task)
        job = await jt
        assert isinstance(job, ContextualizationJob)
        assert isinstance(job.result, list)
        assert {"data", "score", "target"} == job.result[0].keys()
        RTAPI.delete(model)
