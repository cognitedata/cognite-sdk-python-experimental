import re

import pytest

from cognite.experimental import CogniteClient

@pytest.fixture
def sources():
    return [
        {
            "id": 1,
            "name": "prefix_12_AB_0001/suffix",
        },
        {
            "id": 2,
            "name": "prefix_12_AB_0002/suffix",
        }
    ]

@pytest.fixture
def targets():
    return [
        {
            "id": 1,
            "name": "12_AB_0001",
        },
        {
            "id": 2,
            "name": "12_AB_0002",
        }
    ]

@pytest.fixture
def rules():
    return {
        "rules": [
            {
                "extractors": [
                    {
                        "entitySet": "sources",
                        "extractorType": "regex",
                        "field": "name",
                        "pattern": "^[A-Z]+_([0-9]+)_([A-Z]+)_([0-9]+)(.*)$"
                    },
                    {
                        "entitySet": "targets",
                        "extractorType": "regex",
                        "field": "name",
                        "pattern": "^([0-9]+)_([A-Z]+)_([0-9]+)$"
                    }
                ],
                "conditions": [
                    {"conditionType": "equals", "arguments": [{"indices": [0, 0]}, {"indices": [1, 0]}]},
                    {"conditionType": "equals", "arguments": [{"indices": [0, 1]}, {"indices": [1, 1]}]},
                    {"conditionType": "equals", "arguments": [{"indices": [0, 2]}, {"indices": [1, 2]}]},
                ]
            }
        ],
        "priorities": [30]
    }

@pytest.fixture
def reference_matches():
    return [{"sourceId": i, "targetId": i} for i in [1, 2]]

@pytest.fixture
def matches(sources, targets):
    return {0: [{"sources": s, "targets": t} for s, t in zip(sources, targets)]}

@pytest.fixture
def info():
    return {0: {"numberOfMatches": 2, "conflicts": {}, "overlaps": {}}}

COGNITE_CLIENT = CogniteClient()
RULES_API = COGNITE_CLIENT.match_rules


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
def mock_status_apply_ok(rsps, matches, info):
    response_body = {
        "jobId": 121110,
        "status": "Completed",
        "matches": matches,
        "info": info
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
        "rulees": rules,
    }
    rsps.add(
        rsps.GET,
        re.compile(RULES_API._get_base_url_with_base_path() + RULES_API._RESOURCE_PATH + "/suggest" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps




class TestMatchRules:
    def test_suggest(self, sources, targets, matches):
        

