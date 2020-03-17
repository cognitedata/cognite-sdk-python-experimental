import asyncio
import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
EEAPI = COGNITE_CLIENT.entity_extraction


@pytest.fixture
def mock_extract(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        EEAPI._get_base_url_with_base_path() + EEAPI._RESOURCE_PATH + "/extract",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed"}
    rsps.add(
        rsps.GET,
        re.compile(EEAPI._get_base_url_with_base_path() + EEAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"jobId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(EEAPI._get_base_url_with_base_path() + EEAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestEntityExtraction:
    @pytest.mark.asyncio
    async def test_extract(self, mock_extract, mock_status_ok):
        entities = ["a", "b"]
        file_ids = [1, 2]
        resp = EEAPI.extract(file_ids, entities)
        assert isinstance(resp, asyncio.Task)
        job = await resp
        assert isinstance(job, ContextualizationJob)
        assert "Completed" == job.status
        assert 123 == job.job_id

        extract_calls = 0
        n_status_calls = 0
        for call in mock_extract.calls:
            if "extract" in call.request.url:
                extract_calls += 1
                assert {"entities": entities, "fileIds": file_ids} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls

    @pytest.mark.asyncio
    async def test_run_fails(self, mock_extract, mock_status_failed):
        task = EEAPI.extract([1], [])
        with pytest.raises(ModelFailedException) as exc_info:
            await task
        assert "Job 123 failed with error 'error message'" == str(exc_info.value)
