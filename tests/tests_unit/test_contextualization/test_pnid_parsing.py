import re
import unittest

import pytest
from cognite.client.data_classes import ContextualizationJob
from cognite.client.exceptions import ModelFailedException

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import PNIDDetectionList, PNIDDetectResults
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing


@pytest.fixture
def mock_detect(rsps):
    response_body = {"jobId": 789, "status": "Queued"}
    rsps.add(
        rsps.POST,
        PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/detect",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_extract_pattern(rsps):
    response_body = {"jobId": 456, "status": "Queued"}
    rsps.add(
        rsps.POST,
        PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/extractpattern",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_convert(rsps):
    response_body = {"jobId": 345, "status": "Queued"}
    rsps.add(
        rsps.POST,
        PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/convert",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_detect_ok(rsps):
    response_body = {
        "jobId": 123,
        "status": "Completed",
        "items": [
            {"text": "a", "boundingBox": {"xMin": 0, "xMax": 1, "yMin": 0, "yMax": 1}, "entities": [{"name": "a"}]}
        ],
        "fileId": 123432423,
        "fileExternalId": "123432423",
    }
    rsps.add(
        rsps.GET,
        re.compile(PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/detect" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_pattern_ok(rsps):
    response_body = {
        "jobId": 456,
        "status": "Completed",
        "items": [],
        "fileId": 123432423,
        "fileExternalId": "123432423",
    }
    rsps.add(
        rsps.GET,
        re.compile(PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/extractpattern" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_convert_ok(rsps):
    response_body = {
        "jobId": 123,
        "status": "Completed",
        "svgUrl": "svg.url.com",
        "pngUrl": "png.url.com",
        "fileId": 123432423,
        "fileExternalId": "123432423",
    }
    rsps.add(
        rsps.GET,
        re.compile(PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/convert" + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"jobId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(PNIDAPI._get_base_url_with_base_path() + PNIDAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPNIDParsing:
    def test_detect_entities_str(self, mock_detect, mock_status_detect_ok):
        entities = ["a", "b"]
        file_id = 123432423
        job = PNIDAPI.detect(
            file_id=file_id, entities=entities, name_mapping={"a": "c"}, partial_match=False, min_tokens=3
        )
        assert isinstance(job, ContextualizationJob)
        assert "items" in job.result
        assert 789 == job.job_id
        assert "Completed" == job.status

        n_detect_calls = 0
        n_status_calls = 0
        for call in mock_detect.calls:
            if "detect" in call.request.url and call.request.method == "POST":
                n_detect_calls += 1
                assert {
                    "entities": entities,
                    "fileId": file_id,
                    "nameMapping": {"a": "c"},
                    "partialMatch": False,
                    "minTokens": 3,
                    "searchField": "name",
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/789" in call.request.url
        assert 1 == n_detect_calls
        assert 1 == n_status_calls

    def test_detect_entities_dict(self, mock_detect, mock_status_detect_ok):
        entities = [{"name": "a"}, {"name": "b"}]
        file_id = 123432423
        job = PNIDAPI.detect(
            file_id=file_id, entities=entities, name_mapping={"a": "c"}, partial_match=False, min_tokens=3
        )
        assert isinstance(job, ContextualizationJob)
        assert "items" in job.result
        assert 789 == job.job_id
        assert "Completed" == job.status

        assert 1 == len(job.matches)
        assert [{"name": "a"}] == job.matches[0].entities
        assert "a" == job.matches[0].text

        n_detect_calls = 0
        n_status_calls = 0
        for call in mock_detect.calls:
            if "detect" in call.request.url and call.request.method == "POST":
                n_detect_calls += 1
                assert {
                    "entities": [{"name": "a"}, {"name": "b"}],
                    "fileId": file_id,
                    "nameMapping": {"a": "c"},
                    "partialMatch": False,
                    "minTokens": 3,
                    "searchField": "name",
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/789" in call.request.url
        assert 1 == n_detect_calls
        assert 1 == n_status_calls

    def test_extract_pattern(self, mock_extract_pattern, mock_status_pattern_ok):
        patterns = ["ab{1,2}"]
        file_id = 123432423
        job = PNIDAPI.extract_pattern(file_id=file_id, patterns=patterns)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "items" in job.result
        assert "Completed" == job.status
        assert 456 == job.job_id

        n_extract_pattern_calls = 0
        n_status_calls = 0
        for call in mock_extract_pattern.calls:
            if "extractpattern" in call.request.url and call.request.method == "POST":
                n_extract_pattern_calls += 1
                assert {"patterns": patterns, "fileId": file_id} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/456" in call.request.url
        assert 1 == n_extract_pattern_calls
        assert 1 == n_status_calls

    def test_convert(self, mock_convert, mock_status_convert_ok):
        items = [
            {
                "text": "21-PT-1019",
                "boundingBox": {
                    "xMax": 0.5895183277794608,
                    "xMin": 0.573159648591336,
                    "yMax": 0.3737254901960784,
                    "yMin": 0.3611764705882352,
                },
            }
        ]
        file_id = 123432423
        job = PNIDAPI.convert(file_id=file_id, items=items, grayscale=True)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "svgUrl" in job.result
        assert "Completed" == job.status
        assert 345 == job.job_id

        n_convert_calls = 0
        n_status_calls = 0
        for call in mock_convert.calls:
            if "convert" in call.request.url and call.request.method == "POST":
                n_convert_calls += 1
                assert {"fileId": file_id, "items": items, "grayscale": True,} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/345" in call.request.url
        assert 1 == n_convert_calls
        assert 1 == n_status_calls

    def test_file_external_id(self, mock_detect, mock_status_detect_ok):
        entities = [{"name": "a"}, {"name": "b"}]
        file_external_id = "123432423"
        job = PNIDAPI.detect(
            file_external_id=file_external_id,
            entities=entities,
            name_mapping={"a": "c"},
            partial_match=False,
            min_tokens=3,
        )
        assert isinstance(job, PNIDDetectResults)
        assert isinstance(job._repr_html_(), str)
        assert "fileId" in job.result
        assert "fileExternalId" in job.result
        assert file_external_id == job.file_external_id
        assert isinstance(job.matches, PNIDDetectionList)
        assert "Completed" == job.status
