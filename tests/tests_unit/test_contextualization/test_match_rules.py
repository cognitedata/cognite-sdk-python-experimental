import re
import unittest

import pytest
from cognite.client.data_classes import ContextualizationJob

from cognite.experimental import CogniteClient
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
RULES_API = COGNITE_CLIENT.match_rules


@pytest.fixture
def sources():
    return [{"id": 1, "name": "prefix_12_AB_0001/suffix",}, {"id": 2, "name": "prefix_12_AB_0002/suffix",}]


@pytest.fixture
def targets():
    return [{"id": 1, "name": "12_AB_0001",}, {"id": 2, "name": "12_AB_0002",}]


@pytest.fixture
def rules():
    return [
        {
            "extractors": [
                {
                    "entitySet": "sources",
                    "extractorType": "regex",
                    "field": "name",
                    "pattern": "^[a-z]+_([0-9]+)_([A-Z]+)_([0-9]+)(.*)$",
                },
                {
                    "entitySet": "targets",
                    "extractorType": "regex",
                    "field": "name",
                    "pattern": "^([0-9]+)_([A-Z]+)_([0-9]+)$",
                },
            ],
            "conditions": [
                {"conditionType": "equals", "arguments": [[0, 0], [1, 0]]},
                {"conditionType": "equals", "arguments": [[0, 1], [1, 1]]},
                {"conditionType": "equals", "arguments": [[0, 2], [1, 2]]},
            ],
            "priority": 30,
        }
    ]


@pytest.fixture
def reference_matches():
    return [{"sourceId": i, "targetId": i} for i in [1, 2]]


@pytest.fixture
def matches(sources, targets):
    return [{"sources": s, "targets": t} for s, t in zip(sources, targets)]


@pytest.fixture
def result_mock(matches, rules):
    return [{"flags": [], "numberOfMatches": 2, "conflicts": {}, "overlaps": {}, "matches": matches, "rule": rules[0]}]


@pytest.fixture
def mock_apply(rsps):
    response_body = {"jobId": 121110, "status": "Queued"}
    rsps.add(
        rsps.POST,
        RULES_API._get_base_url_with_base_path() + RULES_API._RESOURCE_PATH + "/apply",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_suggest(rsps):
    response_body = {"jobId": 101112, "status": "Queued"}
    rsps.add(
        rsps.POST,
        RULES_API._get_base_url_with_base_path() + RULES_API._RESOURCE_PATH + "/suggest",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_apply_ok(rsps, result_mock):
    response_body = {
        "jobId": 121110,
        "status": "Completed",
        "items": result_mock,
    }
    rsps.add(
        rsps.GET,
        re.compile(RULES_API._get_base_url_with_base_path() + RULES_API._RESOURCE_PATH + "/apply" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_suggest_ok(rsps, rules):
    response_body = {
        "jobId": 121110,
        "status": "Completed",
        "rules": rules,
    }
    rsps.add(
        rsps.GET,
        re.compile(RULES_API._get_base_url_with_base_path() + RULES_API._RESOURCE_PATH + "/suggest" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestMatchRules:
    def test_suggest(self, sources, targets, reference_matches, mock_suggest, mock_status_suggest_ok):
        job = RULES_API.suggest(sources=sources, targets=targets, matches=reference_matches)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "rules" in job.result
        assert "Completed" == job.status
        assert 101112 == job.job_id

        n_suggest_calls = 0
        n_status_calls = 0
        for call in mock_suggest.calls:
            if call.request.method == "POST":
                n_suggest_calls += 1
                assert {"sources": sources, "targets": targets, "matches": reference_matches} == jsgz_load(
                    call.request.body
                )
            else:
                n_status_calls += 1
                assert "/101112" in call.request.url
        assert 1 == n_suggest_calls
        assert 1 == n_status_calls

    def test_apply(self, sources, targets, rules, mock_apply, mock_status_apply_ok):
        job = RULES_API.apply(sources=sources, targets=targets, rules=rules)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "items" in job.result
        assert "Completed" == job.status
        assert 121110 == job.job_id

        n_apply_calls = 0
        n_status_calls = 0
        for call in mock_apply.calls:
            if call.request.method == "POST":
                n_apply_calls += 1
                assert {"sources": sources, "targets": targets, "rules": rules} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/121110" in call.request.url
        assert 1 == n_apply_calls
        assert 1 == n_status_calls
