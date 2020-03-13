import asyncio

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
EEAPI = COGNITE_CLIENT.entity_extraction


class TestEntityExtractionIntegration:
    @pytest.mark.skip("needs unstructured to be enabled")
    @pytest.mark.asyncio
    async def test_extract(self):
        entities = ["a", "b"]
        file_ids = [16072749627134]
        resp = EEAPI.run(file_ids, entities)
        assert isinstance(resp, asyncio.Task)
        job = await resp
        assert isinstance(job, ContextualizationJob)
        assert "Completed" == job.status

    @pytest.mark.asyncio
    async def test_run_fails(self):
        task = EEAPI.run([1], [])
        with pytest.raises(ModelFailedException) as exc_info:
            await task
        assert "failed with error" in str(exc_info.value)
