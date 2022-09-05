import re

import pytest
from cognite.client.data_classes import ContextualizationJob

from tests.utils import jsgz_load


@pytest.fixture
def pnid_object_detection_api(cognite_client):
    return cognite_client.pnid_object_detection


@pytest.fixture
def mock_find_objects(rsps, pnid_object_detection_api):
    response_body = {"jobId": 789, "status": "Queued"}
    rsps.add(
        rsps.POST,
        pnid_object_detection_api._get_base_url_with_base_path()
        + pnid_object_detection_api._RESOURCE_PATH
        + "/findobjects",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_find_objects_ok(rsps, pnid_object_detection_api):
    response_body = {"jobId": 789, "status": "Completed", "fileId": 123432423, "items": []}
    rsps.add(
        rsps.GET,
        re.compile(
            pnid_object_detection_api._get_base_url_with_base_path()
            + pnid_object_detection_api._RESOURCE_PATH
            + "/findobjects/"
        ),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps, pnid_object_detection_api):
    response_body = {"jobId": 789, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(
            pnid_object_detection_api._get_base_url_with_base_path()
            + pnid_object_detection_api._RESOURCE_PATH
            + "/findobjects/"
        ),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPNIDObjectDetection:
    def test_find_objects(self, mock_find_objects, mock_status_find_objects_ok, pnid_object_detection_api):
        file_id = 123432423
        job = pnid_object_detection_api.find_objects(file_id)
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
                assert {
                    "fileId": file_id,
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/789" in call.request.url
        assert 1 == n_find_objects_calls
        assert 1 == n_status_calls
