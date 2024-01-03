import re

import pytest

from cognite.client.data_classes import ContextualizationJob
from cognite.experimental import CogniteClient
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


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


@pytest.fixture
def mock_suggest_ok(rsps):
    response_body = {"items": []}
    rsps.add(
        rsps.POST,
        re.compile(".*?/suggestfields"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_fit(rsps):
    response_body = {"id": 123, "status": "Queued", "createdTime": 42}
    rsps.add(
        rsps.POST, EMAPI._get_base_url_with_base_path() + EMAPI._RESOURCE_PATH + "/", status=200, json=response_body
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"id": 123, "status": "Completed", "createdTime": 42, "statusTime": 456, "startTime": 789}
    rsps.add(
        rsps.GET,
        re.compile(f"{EMAPI._get_base_url_with_base_path()}{EMAPI._RESOURCE_PATH}/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestEntityMatching:
    def test_rules(self, mock_rules, mock_status_rules_ok):
        job = EMAPI.create_rules({"a": "b"})
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert 456 == job.job_id
        assert "ContextualizationJob(id=456, status=Queued, error=None)" == str(job)
        assert {"items": [1]} == job.result
        assert "Completed" == job.status

    def test_suggest_fields(self, mock_suggest_ok):
        res = EMAPI.suggest_fields(sources=[{"name": "a"}], targets=[{"name": "b"}])
        assert {"sources": [{"name": "a"}], "targets": [{"name": "b"}], "scoreThreshold": 0.5} == jsgz_load(
            mock_suggest_ok.calls[0].request.body
        )
        assert isinstance(res, list)

    def test_fit(self, mock_fit, mock_status_ok):  # dup for replacements test, remove/move if that gets to v1
        entities_from = [{"id": 1, "name": "xx"}]
        entities_to = [{"id": 2, "name": "yy"}]
        model = EMAPI.fit(
            sources=entities_from,
            targets=entities_to,
            true_matches=[(1, 2)],
            feature_type="bigram",
            replacements=[{"field": "*", "from": "BADUK", "to": "GO"}],
        )
        assert "EntityMatchingModel(id=123, status=Queued, error=None)" == str(model)
        assert 42 == model.created_time
        model.wait_for_completion()
        assert "Completed" == model.status
        assert 123 == model.id
        assert 42 == model.created_time
        assert 456 == model.status_time
        assert 789 == model.start_time

        n_fit_calls = 0
        n_status_calls = 0
        for call in mock_fit.calls:
            if call.request.method == "POST":
                n_fit_calls += 1
                assert {
                    "sources": entities_from,
                    "targets": entities_to,
                    "trueMatches": [{"sourceId": 1, "targetId": 2}],
                    "featureType": "bigram",
                    "ignoreMissingFields": False,
                    "matchFields": None,
                    "name": None,
                    "description": None,
                    "externalId": None,
                    "classifier": None,
                    "replacements": [{"field": "*", "from": "BADUK", "to": "GO"}],
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == n_fit_calls
        assert 1 == n_status_calls
