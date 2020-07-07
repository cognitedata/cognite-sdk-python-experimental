import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
SCAPI = COGNITE_CLIENT.schemas


@pytest.fixture
def mock_complete(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/complete",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed", "items": []}
    rsps.add(
        rsps.GET,
        re.compile(SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestSchemaCompletion:
    def test_complete(self, mock_complete, mock_status_ok):
        eid = "schematocomplete"
        job = SCAPI.complete(external_id=eid)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items": []} == job.result
        assert "Completed" == job.status
        assert 123 == job.job_id

        extract_calls = 0
        n_status_calls = 0
        for call in mock_complete.calls:
            if call.request.method == "POST":
                extract_calls += 1
                assert {"externalId": eid} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls
