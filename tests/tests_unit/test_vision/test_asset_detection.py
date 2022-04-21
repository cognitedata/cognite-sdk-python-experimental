import json
import re
from unittest.mock import MagicMock

import pytest
from cognite.client.data_classes.contextualization import JobStatus

from cognite.experimental import CogniteClient
from cognite.experimental._api.vision import VisionAPI
from cognite.experimental.data_classes.vision import (
    CreatedDetectAssetsInFilesJob,
    DetectAssetsInFilesJob,
    ExternalFileId,
    InternalFileId,
)

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


@pytest.fixture
def create_job_response_ok():
    return {
        "status": JobStatus.QUEUED.value,
        "createdTime": 934875934785,
        "startTime": 934875934785,
        "statusTime": 934875934785,
        "jobId": 1,
        "items": [
            {"fileId": 1},
            {"fileId": 2, "fileExternalId": "some_external_id"},
            {"fileId": 3},
            {"fileId": 4},
            {"fileId": 5, "fileExternalId": "another"},
        ],
        "useCache": True,
        "partialMatch": True,
        "assetSubtreeIds": [39468345],
    }


@pytest.fixture
def fetch_job_response_ok():
    return {
        "status": JobStatus.COMPLETED.value,
        "createdTime": 934875934785,
        "startTime": 934875934785,
        "statusTime": 934875934785,
        "jobId": 1,
        "items": [
            {
                "fileId": 1,
                "annotations": [{"text": "testing", "assetIds": [1, 2, 3], "confidence": 0.9}],
            },
        ],
        "useCache": True,
        "partialMatch": True,
        "assetSubtreeIds": [39468345],
    }


@pytest.fixture
def mock_create_job_ok(rsps, create_job_response_ok):
    rsps.add(
        rsps.POST,
        re.compile(".*?/context/vision/tagdetection"),
        status=200,
        json=create_job_response_ok,
    )
    yield rsps


@pytest.fixture
def mock_fetch_job_ok(rsps, fetch_job_response_ok):
    rsps.add(
        rsps.GET,
        re.compile(".*?/context/vision/tagdetection"),
        status=200,
        json=fetch_job_response_ok,
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
        if id is not None and hasattr(file, "file_id"):
            if getattr(file, "file_id") == id:
                return True
        if external_id is not None and hasattr(file, "file_external_id"):
            if getattr(file, "file_external_id") == external_id:
                return True

    return False


class TestAssetDetection:
    def test_create_job(self, mock_create_job_ok):
        job = VAPI.detect_assets_in_files(
            files=[
                {"file_id": 1, "file_external_id": "some_external_id"},
                {"file_id": 2},
                {"file_id": 3},
                {"file_id": 4, "file_external_id": "another"},
            ]
        )
        assert isinstance(job, CreatedDetectAssetsInFilesJob), "wrong instance returned"
        assert job.status == JobStatus.QUEUED.value, job
        assert job.job_id > 0, job
        assert contains_file_id(job.items, external_id="some_external_id"), job
        assert contains_file_id(job.items, id=2), job
        assert contains_file_id(job.items, id=3), job
        assert contains_file_id(job.items, external_id="another"), job
        assert job.use_cache, job
        assert job.partial_match, job
        assert 39468345 in job.asset_subtree_ids, job

    def test_retrieve_job(self, mock_fetch_job_ok):
        job = VAPI.retrieve_detected_assets_in_files_job(job_id=1)
        assert isinstance(job, DetectAssetsInFilesJob), "wrong instance returned"
        assert job.status == JobStatus.COMPLETED.value, job
        assert job.items is not None, job
        assert job.job_id == 1, job
        assert contains_file_id(job.items, id=1), job
        assert job.use_cache, job
        assert job.partial_match, job
        assert 39468345 in job.asset_subtree_ids, job

    def test_request_to_camel_case(self):
        expected_request = {"items": [{"fileId": 1}, {"fileExternalId": "abc_test"}]}

        request = VisionAPI._prepare_detect_assets_in_files_request(
            files=[{"file_id": 1}, {"file_external_id": "abc_test"}]  # type: ignore
        )
        assert request == expected_request

        request = VisionAPI._prepare_detect_assets_in_files_request(
            files=[InternalFileId(file_id=1), ExternalFileId(file_external_id="abc_test")]
        )
        assert request == expected_request
