import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import FunctionList

COGNITE_CLIENT = CogniteClient()
FUNCTIONS_API = COGNITE_CLIENT.functions


@pytest.fixture
def mock_functions_response(rsps):
    response_body = {
        "items": [
            {
                "name": "myfunction",
                "externalId": "func-no-123",
                "description": "my fabulous function",
                "status": "Ready",
                "fileId": 1234,
                "createdTime": 1585662507939,
                "apiKey": "***",
                "secrets": {"key1": "***", "key2": "***"},
            }
        ]
    }

    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions"
    rsps.add(rsps.GET, url, status=200, json=response_body)
    yield rsps


class TestFunctionsAPI:
    def test_list(self, mock_functions_response):
        res = FUNCTIONS_API.list()

        assert isinstance(res, FunctionList)
        assert mock_functions_response.calls[0].response.json()["items"] == res.dump(camel_case=True)
