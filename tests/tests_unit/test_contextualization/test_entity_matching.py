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
    response_body = {"modelId": 123, "status": "Queued", "requestTimestamp": 42}
    rsps.add(
        rsps.POST, EMAPI._get_base_url_with_base_path() + EMAPI._RESOURCE_PATH + "/fit", status=200, json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {
        "modelId": 123,
        "status": "Completed",
        "requestTimestamp": 42,
        "statusTimestamp": 456,
        "startTimestamp": 789,
    }
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
        entities_from = [{"id": 1, "name": "xx"}]
        entities_to = [{"id": 2, "name": "yy"}]
        model = EMAPI.fit(match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], feature_type="bigram")
        assert isinstance(model, EntityMatchingModel)
        assert "EntityMatchingModel(id: 123,status: Queued,error: None)" == str(model)
        assert 42 == model.request_timestamp
        model.wait_for_completion()
        assert "Completed" == model.status
        assert 123 == model.model_id
        assert 42 == model.request_timestamp
        assert 456 == model.status_timestamp
        assert 789 == model.start_timestamp

        n_fit_calls = 0
        n_status_calls = 0
        for call in mock_fit.calls:
            if "fit" in call.request.url:
                n_fit_calls += 1
                assert {
                    "matchFrom": entities_from,
                    "matchTo": entities_to,
                    "trueMatches": [[1, 2]],
                    "featureType": "bigram",
                    "completeMissing": False,
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == n_fit_calls
        assert 1 == n_status_calls

    def test_ml_fit(self, mock_fit, mock_status_ok):
        # fit_ml should produce the same output as fit. Will eventually be removed
        entities_from = [{"id": 1, "name": "xx"}]
        entities_to = [{"id": 2, "name": "yy"}]
        model = EMAPI.fit_ml(
            match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], feature_type="bigram"
        )
        assert isinstance(model, EntityMatchingModel)
        assert "EntityMatchingModel(id: 123,status: Queued,error: None)" == str(model)
        assert 42 == model.request_timestamp
        model.wait_for_completion()
        assert "Completed" == model.status
        assert 123 == model.model_id

    def test_fit_cognite_resource(self, mock_fit):
        entities_from = [TimeSeries(id=1, name="x")]
        entities_to = [Asset(id=1, name="x")]
        EMAPI.fit(match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], feature_type="bigram")
        assert {
            "matchFrom": [entities_from[0].dump()],
            "matchTo": [entities_to[0].dump()],
            "trueMatches": [[1, 2]],
            "featureType": "bigram",
            "completeMissing": False,
        } == jsgz_load(mock_fit.calls[0].request.body)

    def test_fit_fails(self, mock_fit, mock_status_failed):
        entities_from = [{"id": 1, "name": "xx"}]
        entities_to = [{"id": 2, "name": "yy"}]
        model = EMAPI.fit(match_from=entities_from, match_to=entities_to)
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
