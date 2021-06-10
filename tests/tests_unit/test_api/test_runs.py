import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ExtractionPipelineRun, ExtractionPipelineRunList

COGNITE_CLIENT = CogniteClient()
TEST_API = COGNITE_CLIENT.extraction_pipeline_runs


@pytest.fixture
def mock_run_response(rsps):
    response_body = {
        "items": [
            {"status": "seen", "createdTime": 1606994793386},
            {"status": "failure", "createdTime": 1606994773381, "message": "ERROR"},
            {"status": "success", "createdTime": 1606994743201},
            {"status": "seen", "createdTime": 1606994696151},
        ]
    }
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/extpipes/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    yield rsps


@pytest.fixture
def mock_create_run_response(rsps):
    response_body = {"items": [{"status": "success", "createdTime": 1607336889530, "externalId": "test"}]}
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/extpipes/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    yield rsps


@pytest.fixture
def mock_run_empty(rsps):
    response_body = {"items": []}
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/extpipes/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    yield rsps


class TestExtractionPipelines:
    def test_empty_list(self, mock_run_empty):
        res = TEST_API.list(external_id="incorrect")
        assert 0 == len(res)

    def test_list(self, mock_run_response):
        res = TEST_API.list(external_id="test")
        assert isinstance(res[0], ExtractionPipelineRun)
        assert 4 == len(res)

    def test_filter(self, mock_run_response):
        res = TEST_API.list(external_id="test", statuses=["success"])
        assert isinstance(res[0], ExtractionPipelineRun)
        assert 4 == len(res)

    def test_create_single(self, mock_create_run_response):
        res = TEST_API.create(ExtractionPipelineRun(external_id="py test id", status="success"))
        assert isinstance(res, ExtractionPipelineRun)
        assert mock_create_run_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_multiple(self, mock_create_run_response):
        run1 = ExtractionPipelineRun(external_id="py test id", status="success")
        run2 = ExtractionPipelineRun(external_id="py test id", status="seen")

        res = TEST_API.create([run1, run2])
        assert isinstance(res, ExtractionPipelineRunList)
        assert mock_create_run_response.calls[0].response.json()["items"] == res.dump(camel_case=True)
