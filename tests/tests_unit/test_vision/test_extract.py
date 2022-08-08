import re
from logging import exception
from typing import Any, Dict, List, Optional, Union

import pytest
from cognite.client.data_classes.contextualization import JobStatus
from responses import RequestsMock

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.vision import Feature, VisionExtractJob
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


@pytest.fixture
def mock_post_response_body() -> Dict[str, Any]:
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
    }


@pytest.fixture
def mock_get_response_body_ok() -> Dict[str, Any]:
    return {
        "status": JobStatus.COMPLETED.value,
        "createdTime": 934875934785,
        "startTime": 934875934785,
        "statusTime": 934875934785,
        "jobId": 1,
        "items": [
            {
                "fileId": 1,
                "annotations": [
                    {"text": "testing", "assetIds": [1, 2, 3], "confidence": 0.9}
                ],  # TODO: rename to predictions
            },
        ],
        "useCache": True,
        "partialMatch": True,
        "assetSubtreeIds": [39468345],
    }


@pytest.fixture
def mock_post_extract(rsps: RequestsMock, mock_post_response_body: Dict[str, Any]) -> RequestsMock:
    rsps.add(
        rsps.POST,
        re.compile(".*?/context/vision/annotate"),  # TODO: rename to extract
        status=200,
        json=mock_post_response_body,
    )
    yield rsps


@pytest.fixture
def mock_get_extract(rsps: RequestsMock, mock_get_response_body_ok: Dict[str, Any]) -> RequestsMock:
    rsps.add(
        rsps.GET,
        re.compile(".*?/context/vision/annotate/\\d+"),  # TODO: rename to extract
        status=200,
        json=mock_get_response_body_ok,
    )
    yield rsps


class TestExtract:
    @pytest.mark.parametrize(
        "features, error_message",
        [
            ("foo", "features must be one of types \\[<enum 'Feature'>, <class 'list'>\\]"),
            ([Feature.TEXT_DETECTION, "foo"], "feature 'foo' must be one of types \\[<enum 'Feature'>]"),
            (None, "features cannot be None"),
            (Feature.TEXT_DETECTION, None),
            ([Feature.TEXT_DETECTION, Feature.PERSONAL_PROTECTIVE_EQUIPMENT_DETECTION], None),
        ],
        ids=[
            "invalid_feature",
            "invalid_non_supported_type_in_list",
            "invalid_feature_None_value",
            "one_feature",
            "multiple_features",
        ],
    )
    def test_extract(
        self,
        mock_post_extract: RequestsMock,
        mock_get_extract: RequestsMock,
        features: Union[Feature, List[Feature]],
        error_message: Optional[str],
    ) -> None:
        file_ids = [1, 2, 3]
        file_external_ids = []
        if error_message is not None:
            with pytest.raises(TypeError, match=error_message):
                VAPI.extract(features=features, file_ids=file_ids, file_external_ids=file_external_ids)
        else:
            # Job should be queued immediately after a successfully POST
            job = VAPI.extract(features=features, file_ids=file_ids, file_external_ids=file_external_ids)
            # Job should be queued immediately after a successfully POST
            assert isinstance(job, VisionExtractJob)
            assert "Queued" == job.status
            # Wait for job to complete and check its content
            expected_job_id = 1
            job.wait_for_completion(interval=0)
            assert "items" in job.result
            assert JobStatus.COMPLETED == JobStatus(job.status)
            assert expected_job_id == job.job_id

            num_post_requests, num_get_requests = 0, 0
            for call in mock_post_extract.calls:
                if "annotate" in call.request.url and call.request.method == "POST":  # TODO: rename to extract
                    num_post_requests += 1
                    assert {
                        "features": [f.value for f in features] if isinstance(features, list) else [features.value],
                        "items": [{"fileId": fid} for fid in file_ids],
                    } == jsgz_load(call.request.body)
                else:
                    num_get_requests += 1
                    assert f"/{expected_job_id}" in call.request.url
            assert 1 == num_post_requests
            assert 1 == num_get_requests

    def test_get_extract(
        self,
        mock_post_extract: RequestsMock,
        mock_get_extract: RequestsMock,
    ) -> None:
        file_ids = [1, 2, 3]
        file_external_ids = []

        job = VAPI.extract(features=Feature.TEXT_DETECTION, file_ids=file_ids, file_external_ids=file_external_ids)

        # retrieved job should correspond to the started job:
        retrieved_job = VAPI.get_extract_job(job_id=job.job_id)

        assert isinstance(retrieved_job, VisionExtractJob)
        assert retrieved_job.job_id == job.job_id

        num_get_requests = 0
        for call in mock_get_extract.calls:
            if "annotate" in call.request.url and call.request.method == "GET":  # TODO: rename to extract
                num_get_requests += 1
                assert f"/{job.job_id}" in call.request.url
        assert 1 == num_get_requests
