import re

import pytest
from cognite.client.data_classes import ContextualizationJob
from cognite.client.exceptions import ModelFailedException

from tests.utils import jsgz_load


@pytest.fixture
def document_api(cognite_client):
    return cognite_client.document_parsing


@pytest.fixture
def mock_detect(rsps, document_api):
    response_body = {"jobId": 456, "status": "Queued"}
    rsps.add(
        rsps.POST,
        document_api._get_base_url_with_base_path() + document_api._RESOURCE_PATH + "/detect",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps, document_api):
    response_body = {"jobId": 123, "status": "Completed", "svgUrl": "x"}
    rsps.add(
        rsps.GET,
        re.compile(document_api._get_base_url_with_base_path() + document_api._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps, document_api):
    response_body = {"jobId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(document_api._get_base_url_with_base_path() + document_api._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPNIDParsing:
    def test_detect(self, mock_detect, mock_status_ok, document_api):
        entities = ["a", "b"]
        file_id = 123432423
        job = document_api.detect(file_id, entities, name_mapping={"a": "c"}, partial_match=False)
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
                    "searchField": "name",
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/456" in call.request.url
        assert 1 == n_detect_calls
        assert 1 == n_status_calls

    def test_run_fails(self, mock_detect, mock_status_failed, document_api):
        job = document_api.detect([1], [])
        with pytest.raises(ModelFailedException) as exc_info:
            job.result
        assert "ContextualizationJob 456 failed with error 'error message'" == str(exc_info.value)
