import os

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Function, FunctionList

COGNITE_CLIENT = CogniteClient()
FUNCTIONS_API = COGNITE_CLIENT.functions
FILES_API = COGNITE_CLIENT.files


EXAMPLE_FUNCTION = {
    "id": 1233456,
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

    def test_list(self, mock_functions_list_response):
        res = FUNCTIONS_API.list()

        assert isinstance(res, FunctionList)
        assert mock_functions_list_response.calls[0].response.json()["items"] == res.dump(camel_case=True)
