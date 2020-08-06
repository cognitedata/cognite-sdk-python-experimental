import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
DOCUMENT_API = COGNITE_CLIENT.document_parsing


@pytest.fixture
def mock_detect(rsps):
    response_body = {"jobId": 456, "status": "Queued"}
    rsps.add(
        rsps.POST,
        DOCUMENT_API._get_base_url_with_base_path() + DOCUMENT_API._RESOURCE_PATH + "/detect",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed", "svgUrl": "x"}
    rsps.add(
        rsps.GET,
        re.compile(DOCUMENT_API._get_base_url_with_base_path() + DOCUMENT_API._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"jobId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(DOCUMENT_API._get_base_url_with_base_path() + DOCUMENT_API._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPNIDParsing:
    def test_detect(self, mock_detect, mock_status_ok):
        entities = ["a", "b"]
        file_id = 123432423
        job = DOCUMENT_API.detect(file_id, entities, name_mapping={"a": "c"}, partial_match=False)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"svgUrl": "x"} == job.result
        assert "Completed" == job.status
        assert 456 == job.job_id

        n_detect_calls = 0
        n_status_calls = 0
        for call in mock_detect.calls:
            if "detect" in call.request.url:
                n_detect_calls += 1
                assert {
                    "entities": entities,
                    "fileId": file_id,
                    "nameMapping": {"a": "c"},
                    "partialMatch": False,
                    "minTokens": 1,
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/456" in call.request.url
        assert 1 == n_detect_calls
        assert 1 == n_status_calls

    def test_run_fails(self, mock_detect, mock_status_failed):
        job = DOCUMENT_API.detect([1], [])
        with pytest.raises(ModelFailedException) as exc_info:
            job.result
        assert "ContextualizationJob 123 failed with error 'error message'" == str(exc_info.value)
