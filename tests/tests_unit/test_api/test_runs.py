import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import IntegrationRun, IntegrationRunList, IntegrationWithStatuses, IntegrationWithStatusesList
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
TEST_API = COGNITE_CLIENT.runs


@pytest.fixture
def mock_run_response(rsps):
    response_body = {
        "items": [
            {
                "externalId": "test",
                "createdTime": 1606994621658,
                "lastUpdatedTime": 1606994621658,
                "statuses": [
                    {
                        "status": "seen",
                        "createdTime": 1606994793386
                    },
                    {
                        "status": "failure",
                        "createdTime": 1606994773381
                    },
                    {
                        "status": "success",
                        "createdTime": 1606994743201
                    },
                    {
                        "status": "seen",
                        "createdTime": 1606994696151
                    }
                ]
            }
        ]
    }
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/integrations/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    yield rsps

@pytest.fixture
def mock_create_run_response(rsps):
    response_body = {
        "items": [
            {
                "status": "success",
                "createdTime": 1607336889530,
                "externalId": "test"
            }
        ]
    }
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/integrations/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    yield rsps


@pytest.fixture
def mock_run_empty(rsps):
    response_body = {"items": []}
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path())
        + r"/integrations/runs(?:/?.+|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    yield rsps


class TestIntegrations:
    def test_empty_list(self, mock_run_empty):
        res = TEST_API.list(external_id="incorrect")
        assert 0 == len(res)

    def test_list(self, mock_run_response):
        res = TEST_API.list(external_id="test")
        assert isinstance(res[0], IntegrationRun)
        assert 4 == len(res)

    def test_create_single(self, mock_create_run_response):
        res = TEST_API.create(
            IntegrationRun(external_id="py test id",
                           status="success"
                           )
        )
        assert isinstance(res, IntegrationRun)
        assert mock_create_run_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_multiple(self, mock_create_run_response):
        run1 = IntegrationRun(external_id="py test id",
                              status="success"
                              )
        run2 = IntegrationRun(external_id="py test id",
                              status="seen"
                              )

        res = TEST_API.create([run1, run2])
        assert isinstance(res, IntegrationRunList)
        assert mock_create_run_response.calls[0].response.json()["items"] == res.dump(camel_case=True)
