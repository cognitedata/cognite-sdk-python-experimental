import re

import pytest
from cognite.client.data_classes import ContextualizationJob

from cognite.experimental import CogniteClient

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


class TestEntityMatching:
    def test_rules(self, mock_rules, mock_status_rules_ok):
        job = EMAPI.create_rules({"a": "b"})
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert 456 == job.job_id
        assert "ContextualizationJob(id: 456,status: Queued,error: None)" == str(job)
        assert {"items": [1]} == job.result
        assert "Completed" == job.status
