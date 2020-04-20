import re

import pytest

from cognite.client.data_classes import Asset, TimeSeries
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
def mock_fit_ml(rsps):
    response_body = {"modelId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        EMAPI._get_base_url_with_base_path() + EMAPI._RESOURCE_PATH + "/fitml",
        status=200,
        json=response_body,
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
    response_body = {"jobId": 456, "status": "Completed", "items": [1]}
    rsps.add(
        rsps.GET,
        re.compile(f"{EMAPI._get_base_url_with_base_path()}{EMAPI._RESOURCE_PATH}/rules/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestEntityMatching:
    def test_fit(self, mock_fit, mock_status_ok):
        entities = ["a", "b"]
        model = EMAPI.fit(entities)
        assert isinstance(model, EntityMatchingModel)
        assert "EntityMatchingModel(id: 123,status: Queued,error: None)" == str(model)
        model.wait_for_completion()
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

    def test_ml_fit(self, mock_fit_ml, mock_status_ok):
        entities_from = [{"id": 1, "name": "xx"}]
        entities_to = [{"id": 2, "name": "yy"}]
        model = EMAPI.fit_ml(match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], model_type="foo")
        assert isinstance(model, EntityMatchingModel)
        assert "EntityMatchingModel(id: 123,status: Queued,error: None)" == str(model)
        model.wait_for_completion()
        assert "Completed" == model.status
        assert 123 == model.model_id

        n_fit_calls = 0
        n_status_calls = 0
        for call in mock_fit_ml.calls:
            if "fit" in call.request.url:
                n_fit_calls += 1
                assert {
                    "matchFrom": entities_from,
                    "matchTo": entities_to,
                    "trueMatches": [[1, 2]],
                    "modelType": "foo",
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == n_fit_calls
        assert 1 == n_status_calls

    def test_ml_fit_cognite_resource(self, mock_fit_ml):
        entities_from = [TimeSeries(id=1, name="x")]
        entities_to = [Asset(id=1, name="x")]
        EMAPI.fit_ml(match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], model_type="foo")
        assert {
            "matchFrom": [entities_from[0].dump()],
            "matchTo": [entities_to[0].dump()],
            "trueMatches": [[1, 2]],
            "modelType": "foo",
        } == jsgz_load(mock_fit_ml.calls[0].request.body)

    def test_fit_fails(self, mock_fit, mock_status_failed):
        model = EMAPI.fit(["a", "b"])
        with pytest.raises(ModelFailedException) as exc_info:
            model.wait_for_completion()
        assert exc_info.type is ModelFailedException
        assert 123 == exc_info.value.id
        assert "error message" == exc_info.value.error_message
        assert "EntityMatchingModel 123 failed with error 'error message'" == str(exc_info.value)

    def test_retrieve(self, mock_status_ok):
        model = EMAPI.retrieve(model_id=123)
        assert isinstance(model, EntityMatchingModel)
        assert "Completed" == model.status
        assert 123 == model.model_id

    def test_rules(self, mock_rules, mock_status_rules_ok):
        job = EMAPI.create_rules({"a": "b"})
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert 456 == job.job_id
        assert "ContextualizationJob(id: 456,status: Queued,error: None)" == str(job)
        assert {"items": [1]} == job.result
        assert "Completed" == job.status
