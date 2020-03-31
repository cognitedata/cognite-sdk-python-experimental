import asyncio
import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, EntityMatchingModel
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


@pytest.fixture
def mock_fit(rsps):
    response_body = {"modelId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST, EMAPI._get_base_url_with_base_path() + EMAPI._RESOURCE_PATH + "/fit", status=200, json=response_body
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"modelId": 123, "status": "Completed"}
    rsps.add(
        rsps.GET,
        re.compile(f"{EMAPI._get_base_url_with_base_path()}{EMAPI._RESOURCE_PATH}/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"modelId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(f"{EMAPI._get_base_url_with_base_path()}{EMAPI._RESOURCE_PATH}/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_rules(rsps):
    response_body = {"jobId": 456, "status": "Queued"}
    rsps.add(
        rsps.POST,
        EMAPI._get_base_url_with_base_path() + EMAPI._RESOURCE_PATH + "/rules",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_rules_ok(rsps):
    response_body = {"jobId": 456, "status": "Completed"}
    rsps.add(
        rsps.GET,
        re.compile(f"{EMAPI._get_base_url_with_base_path()}{EMAPI._RESOURCE_PATH}/rules/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestEntityMatching:
    @pytest.mark.asyncio
    async def test_fit(self, mock_fit, mock_status_ok):
        entities = ["a", "b"]
        resp = EMAPI.fit(entities)
        assert isinstance(resp, asyncio.Task)
        model = await resp
        assert isinstance(model, EntityMatchingModel)
        assert "ContextualizationModel(id: 123,status: Completed)" == str(model)
        assert "Completed" == model.status
        assert 123 == model.model_id

        n_fit_calls = 0
        n_status_calls = 0
        for call in mock_fit.calls:
            if "fit" in call.request.url:
                n_fit_calls += 1
                assert {"items": entities} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == n_fit_calls
        assert 1 == n_status_calls

    @pytest.mark.asyncio
    async def test_fit_fails(self, mock_fit, mock_status_failed):
        task = EMAPI.fit(["a", "b"])
        with pytest.raises(ModelFailedException) as exc_info:
            await task
        assert exc_info.type is ModelFailedException
        assert 123 == exc_info.value.id
        assert "error message" == exc_info.value.error_message
        assert "Model 123 failed with error 'error message'" == str(exc_info.value)

    def test_retrieve(self, mock_status_ok):
        model = EMAPI.retrieve(model_id=123)
        assert isinstance(model, EntityMatchingModel)
        assert "Completed" == model.status
        assert 123 == model.model_id

    @pytest.mark.asyncio
    async def test_rules(self, mock_rules, mock_status_rules_ok):
        task = EMAPI.create_rules({"a": "b"})
        assert isinstance(task, asyncio.Task)
        job = await task
        assert isinstance(job, ContextualizationJob)
        assert 456 == job.job_id
