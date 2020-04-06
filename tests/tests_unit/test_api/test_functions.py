import os

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Function, FunctionCall, FunctionList
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
FUNCTIONS_API = COGNITE_CLIENT.functions
FILES_API = COGNITE_CLIENT.files


EXAMPLE_FUNCTION = {
    "id": 123456,
    "name": "myfunction",
    "externalId": "func-no-123",
    "description": "my fabulous function",
    "owner": "ola.normann@cognite.com",
    "status": "Ready",
    "fileId": 1234,
    "createdTime": 1585662507939,
    "apiKey": "***",
    "secrets": {"key1": "***", "key2": "***"},
}


@pytest.fixture
def mock_functions_list_response(rsps):
    response_body = {"items": [EXAMPLE_FUNCTION]}

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions"
    rsps.add(rsps.GET, url, status=200, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_retrieve_response(rsps):
    response_body = {"items": [EXAMPLE_FUNCTION]}

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/byids"
    rsps.add(rsps.POST, url, status=200, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_create_response(rsps):
    files_response_body = {
        "name": "myfunction",
        "id": 1234,
        "uploaded": True,
        "createdTime": 1585662507939,
        "lastUpdatedTime": 1585662507939,
        "uploadUrl": "https://upload.here",
    }

    rsps.assert_all_requests_are_fired = False

    files_url = FILES_API._get_base_url_with_base_path() + "/files"
    rsps.add(rsps.POST, files_url, status=201, json=files_response_body)
    rsps.add(rsps.PUT, "https://upload.here", status=200)

    functions_url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions"
    rsps.add(rsps.POST, functions_url, status=201, json={"items": [EXAMPLE_FUNCTION]})

    yield rsps


@pytest.fixture
def mock_functions_delete_response(rsps):
    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/delete"
    rsps.add(rsps.POST, url, status=200, json={})

    yield rsps


@pytest.fixture
def mock_functions_call_completed_response(rsps):
    response_body_sync = {
        "id": 7255309231137124,
        "startTime": 1585925306822,
        "endTime": 1585925310822,
        "response": "Hello World!",
        "status": "Completed",
    }
    response_body_async = response_body_sync.copy()
    del response_body_async["response"]

    url_sync = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/1234/call"
    url_async = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/1234/async_call"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.POST, url_sync, status=201, json=response_body_sync)
    rsps.add(rsps.POST, url_async, status=201, json=response_body_async)

    yield rsps


@pytest.fixture
def mock_functions_call_by_external_id(mock_functions_retrieve_response):
    response_body = {
        "id": 7255309231137124,
        "startTime": 1585925306822,
        "endTime": 1585925310822,
        "response": "Hello World!",
        "status": "Completed",
    }

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/123456/call"
    rsps = mock_functions_retrieve_response
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_call_failed_response(rsps):
    response_body = {
        "id": 7255309231137124,
        "startTime": 1585925306822,
        "endTime": 1585925310822,
        "status": "Failed",
        "error": {"message": "some message", "trace": "some stack trace"},
    }

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/1234/call"
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_call_timeout_response(rsps):
    response_body = {"id": 7255309231137124, "startTime": 1585925306822, "endTime": 1585925310822, "status": "Timeout"}

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/1234/call"
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


class TestFunctionsAPI:
    def test_create_with_path(self, mock_functions_create_response):
        folder = os.path.join(os.path.dirname(__file__), "function_code")
        res = FUNCTIONS_API.create(name="myfunction", folder=folder)

        assert isinstance(res, Function)
        assert mock_functions_create_response.calls[2].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_with_file_id(self, mock_functions_create_response):
        res = FUNCTIONS_API.create(name="myfunction", file_id=1234)

        assert isinstance(res, Function)
        assert mock_functions_create_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_with_path_and_file_id_raises(self, mock_functions_create_response):
        with pytest.raises(TypeError):
            FUNCTIONS_API.create(name="myfunction", folder="some/folder", file_id=1234)

    def test_delete_single_id(self, mock_functions_delete_response):
        res = FUNCTIONS_API.delete(id=1)
        assert {"items": [{"id": 1}]} == jsgz_load(mock_functions_delete_response.calls[0].request.body)

    def test_delete_single_external_id(self, mock_functions_delete_response):
        res = FUNCTIONS_API.delete(external_id="func1")
        assert {"items": [{"externalId": "func1"}]} == jsgz_load(mock_functions_delete_response.calls[0].request.body)

    def test_delete_multiple_id_and_multiple_external_id(self, mock_functions_delete_response):
        res = FUNCTIONS_API.delete(id=[1, 2, 3], external_id=["func1", "func2"])
        assert {
            "items": [{"id": 1}, {"id": 2}, {"id": 3}, {"externalId": "func1"}, {"externalId": "func2"}]
        } == jsgz_load(mock_functions_delete_response.calls[0].request.body)

    def test_list(self, mock_functions_list_response):
        res = FUNCTIONS_API.list()

        assert isinstance(res, FunctionList)
        assert mock_functions_list_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_retrieve_by_id(self, mock_functions_retrieve_response):
        res = FUNCTIONS_API.retrieve(id=1)
        assert isinstance(res, Function)
        assert mock_functions_retrieve_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_retrieve_by_external_id(self, mock_functions_retrieve_response):
        res = FUNCTIONS_API.retrieve(external_id="func1")
        assert isinstance(res, Function)
        assert mock_functions_retrieve_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_retrieve_by_id_and_external_id_raises(self):
        with pytest.raises(AssertionError):
            FUNCTIONS_API.retrieve(id=1, external_id="func1")

    def test_retrieve_multiple_by_ids(self, mock_functions_retrieve_response):
        res = FUNCTIONS_API.retrieve_multiple(ids=[1])
        assert isinstance(res, FunctionList)
        assert mock_functions_retrieve_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_retrieve_multiple_by_external_ids(self, mock_functions_retrieve_response):
        res = FUNCTIONS_API.retrieve_multiple(external_ids=["func1"])
        assert isinstance(res, FunctionList)
        assert mock_functions_retrieve_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_retrieve_multiple_by_ids_and_external_ids(self, mock_functions_retrieve_response):
        res = FUNCTIONS_API.retrieve_multiple(ids=[1], external_ids=["func1"])
        assert isinstance(res, FunctionList)
        assert mock_functions_retrieve_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_function_call(self, mock_functions_call_completed_response):
        res = FUNCTIONS_API.call(id=1234)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_completed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_async_call(self, mock_functions_call_completed_response):
        res = FUNCTIONS_API.call(id=1234, asyncronous=True)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_completed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_call_by_external_id(self, mock_functions_call_by_external_id):
        res = FUNCTIONS_API.call(external_id="func-no-123")
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_by_external_id.calls[1].response.json() == res.dump(camel_case=True)

    def test_function_call_failed(self, mock_functions_call_failed_response):
        res = FUNCTIONS_API.call(id=1234)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_failed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_call_timout(self, mock_functions_call_timeout_response):
        res = FUNCTIONS_API.call(id=1234)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_timeout_response.calls[0].response.json() == res.dump(camel_case=True)
