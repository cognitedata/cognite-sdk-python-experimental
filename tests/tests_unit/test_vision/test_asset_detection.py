import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.vision import (
    CreatedDetectAssetsInFilesJob,
    DetectAssetsInFilesJob,
)

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


@pytest.fixture
def mock_create_job_ok(rsps):
    response_body = {
        "status": "Queued",
        "createdTime": 934875934785,
        "startTime": 934875934785,
        "statusTyime": 934875934785,
        "jobId": 1,
        "items": [
            {"fileId": 1},
            {"fileId": "some_external_id"},
            {"fileId": 234235},
            {"fileId": 23},
            {"fileId": "another"},
        ],
    }
    rsps.add(
        rsps.POST,
        re.compile(".*?/context/vision/tagdetection"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_fetch_job_ok(rsps):
    response_body = {
        "status": "Completed",
        "createdTime": 934875934785,
        "startTime": 934875934785,
        "statusTyime": 934875934785,
        "jobId": 1,
        "items": [
            {
                "fileId": 1,
                "annotations": [{"text": "testing", "assetIds": [1, 2, 3], "confidence": 0.9}],
            },
        ],
    }
    rsps.add(
        rsps.GET,
        re.compile(".*?/context/vision/tagdetection"),
        status=200,
        json=response_body,
    )
    yield rsps


def contains_file_id(
    files,
    id=None,
    external_id=None,
):
    if id is None and external_id is None:
        raise ValueError("id or external_id must be specified")
    if id is not None and external_id is not None:
        raise ValueError("either id or external_id can be specified, not both")

    for file in files:
        if id is not None:
            if file.file_id == id:
                return True
        if external_id is not None:
            if file.file_external_id == external_id:
                return True

    return False


class TestAssetDetection:
    def test_create_job(self, mock_create_job_ok):
        job = VAPI.detect_assets_in_files(
            files=[
                "some_external_id",
                234235,
                23,
                "another",
            ]
        )
        assert isinstance(job, CreatedDetectAssetsInFilesJob), "wrong instance returned"
        assert job.status == "queued"
        assert job.job_id > 0
        assert contains_file_id(job.items, external_id="some_external_id")
        assert contains_file_id(job.items, id=234235)
        assert contains_file_id(job.items, id=23)
        assert contains_file_id(job.items, external_id="another")

    def test_retrieve_job(self, mock_fetch_job_ok):
        job = VAPI.retrieve_detected_assets_in_files_job(job_id=1)
        assert isinstance(job, DetectAssetsInFilesJob), "wrong instance returned"
        assert job.status == "finished"
        assert job.job_id == 1
        assert contains_file_id(job.items, id=1)
