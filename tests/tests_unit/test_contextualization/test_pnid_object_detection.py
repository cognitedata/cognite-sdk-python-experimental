import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
PNID_OBJECT_DETECTION_API = COGNITE_CLIENT.pnid_object_detection


@pytest.fixture
def mock_find_objects(rsps):
    response_body = {"jobId": 789, "status": "Queued"}
    rsps.add(
        rsps.POST,
        PNID_OBJECT_DETECTION_API._get_base_url_with_base_path()
        + PNID_OBJECT_DETECTION_API._RESOURCE_PATH
        + "/findobjects",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_find_objects_ok(rsps):
    response_body = {"jobId": 789, "status": "Completed", "items": []}
    rsps.add(
        rsps.GET,
        re.compile(
            PNID_OBJECT_DETECTION_API._get_base_url_with_base_path()
            + PNID_OBJECT_DETECTION_API._RESOURCE_PATH
            + "/\\d+"
        ),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"jobId": 789, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(
            PNID_OBJECT_DETECTION_API._get_base_url_with_base_path()
            + PNID_OBJECT_DETECTION_API._RESOURCE_PATH
            + "/\\d+"
        ),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPNIDObjectDetection:
    def test_find_objects(self, mock_find_objects, mock_status_find_objects_ok):
        file_id = 123432423
        job = PNID_OBJECT_DETECTION_API.find_objects(file_id)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "items" in job.result
        assert "Completed" == job.status
        assert 789 == job.job_id

        n_find_objects_calls = 0
        n_status_calls = 0
        for call in mock_find_objects.calls:
            if "findobjects" in call.request.url and call.request.method == "POST":
                n_find_objects_calls += 1
                assert {"fileId": file_id,} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/789" in call.request.url
        assert 1 == n_find_objects_calls
        assert 1 == n_status_calls
