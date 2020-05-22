import os

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental._api.functions import validate_function_folder
from cognite.experimental.data_classes import (
    Function,
    FunctionCall,
    FunctionCallList,
    FunctionCallLog,
    FunctionList,
    FunctionSchedule,
    FunctionSchedulesList,
)
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
FUNCTIONS_API = COGNITE_CLIENT.functions
FUNCTION_CALLS_API = FUNCTIONS_API.calls
FUNCTION_SCHEDULES_API = FUNCTIONS_API.schedules
FILES_API = COGNITE_CLIENT.files

FUNCTION_ID = 1234

EXAMPLE_FUNCTION = {
    "id": FUNCTION_ID,
    "name": "myfunction",
    "externalId": f"func-no-{FUNCTION_ID}",
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
        "id": FUNCTION_ID,
        "uploaded": True,
        "createdTime": 1585662507939,
        "lastUpdatedTime": 1585662507939,
        "uploadUrl": "https://upload.here",
    }

    rsps.assert_all_requests_are_fired = False

    files_url = FILES_API._get_base_url_with_base_path() + "/files"
    rsps.add(rsps.POST, files_url, status=201, json=files_response_body)
    rsps.add(rsps.PUT, "https://upload.here", status=201)

    functions_url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions"
    rsps.add(rsps.POST, functions_url, status=201, json={"items": [EXAMPLE_FUNCTION]})

    yield rsps


@pytest.fixture
def mock_functions_delete_response(rsps):
    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/delete"
    rsps.add(rsps.POST, url, status=200, json={})

    yield rsps


BASE_CALL = {
    "id": 5678,
    "startTime": 1585925306822,
    "endTime": 1585925310822,
    "status": "Completed",
    "functionId": FUNCTION_ID,
}


@pytest.fixture
def mock_functions_call_completed_response(rsps):
    response_body_async = BASE_CALL.copy()
    response_body_sync = BASE_CALL.copy()
    response_body_sync["response"] = "Hello World!"

    url_sync = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/call"
    url_async = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/async_call"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.POST, url_sync, status=201, json=response_body_sync)
    rsps.add(rsps.POST, url_async, status=201, json=response_body_async)

    yield rsps


@pytest.fixture
def mock_functions_call_by_external_id(mock_functions_retrieve_response):
    response_body = BASE_CALL.copy()
    response_body["response"] = "Hello World!"

    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/call"
    rsps = mock_functions_retrieve_response
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_call_failed_response(rsps):
    response_body = BASE_CALL.copy()
    response_body["status"] = "Failed"
    response_body["error"] = ({"message": "some message", "trace": "some stack trace"},)

    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/call"
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


@pytest.fixture
def mock_functions_call_timeout_response(rsps):
    response_body = BASE_CALL.copy()
    response_body["status"] = "Timeout"

    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/call"
    rsps.add(rsps.POST, url, status=201, json=response_body)

    yield rsps


@pytest.fixture
def function_handle():
    def handle(data, client, secrets):
        pass

    return handle


@pytest.fixture
def function_handle_illegal_name():
    def func(data, client, secrets):
        pass

    return func


@pytest.fixture
def function_handle_illegal_argument():
    def handle(client, input):
        pass

    return handle


class TestFunctionsAPI:
    @pytest.mark.parametrize(
        "function_folder, will_pass",
        [("function_code", True), ("bad_function_code", False), ("bad_function_code2", False)],
    )
    def test_validate_folder(self, function_folder, will_pass):
        folder = os.path.join(os.path.dirname(__file__), function_folder)
        if will_pass:
            validate_function_folder(folder)
        else:
            with pytest.raises(TypeError):
                validate_function_folder(folder)

    def test_create_with_path(self, mock_functions_create_response):
        folder = os.path.join(os.path.dirname(__file__), "function_code")
        res = FUNCTIONS_API.create(name="myfunction", folder=folder)

        assert isinstance(res, Function)
        assert mock_functions_create_response.calls[2].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_with_file_id(self, mock_functions_create_response):
        res = FUNCTIONS_API.create(name="myfunction", file_id=1234)

        assert isinstance(res, Function)
        assert mock_functions_create_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_with_function_handle(self, mock_functions_create_response, function_handle):
        res = FUNCTIONS_API.create(name="myfunction", function_handle=function_handle)

        assert isinstance(res, Function)
        assert mock_functions_create_response.calls[2].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_with_function_handle_with_illegal_name_raises(self, function_handle_illegal_name):
        with pytest.raises(TypeError):
            FUNCTIONS_API.create(name="myfunction", function_handle=function_handle_illegal_name)

    def test_create_with_function_handle_with_illegal_argument_raises(self, function_handle_illegal_argument):
        with pytest.raises(TypeError):
            FUNCTIONS_API.create(name="myfunction", function_handle=function_handle_illegal_argument)

    def test_create_with_handle_function_and_file_id_raises(self, mock_functions_create_response, function_handle):
        with pytest.raises(TypeError):
            FUNCTIONS_API.create(name="myfunction", function_handle=function_handle, file_id=1234)

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
        res = FUNCTIONS_API.call(id=FUNCTION_ID)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_completed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_async_call(self, mock_functions_call_completed_response):
        res = FUNCTIONS_API.call(id=FUNCTION_ID, asynchronous=True)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_completed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_call_by_external_id(self, mock_functions_call_by_external_id):
        res = FUNCTIONS_API.call(external_id=f"func-no-{FUNCTION_ID}")
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_by_external_id.calls[1].response.json() == res.dump(camel_case=True)

    def test_function_call_failed(self, mock_functions_call_failed_response):
        res = FUNCTIONS_API.call(id=FUNCTION_ID)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_failed_response.calls[0].response.json() == res.dump(camel_case=True)

    def test_function_call_timout(self, mock_functions_call_timeout_response):
        res = FUNCTIONS_API.call(id=FUNCTION_ID)
        assert isinstance(res, FunctionCall)
        assert mock_functions_call_timeout_response.calls[0].response.json() == res.dump(camel_case=True)


@pytest.fixture
def mock_function_calls_list_response(rsps):
    response_body = {"items": [BASE_CALL.copy()]}
    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/calls/list"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.POST, url, status=200, json=response_body)

    yield rsps


@pytest.fixture
def mock_function_calls_retrieve_response(rsps):
    response_body = BASE_CALL.copy()
    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/calls/5678"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.GET, url, status=200, json=response_body)

    yield rsps


@pytest.fixture
def mock_function_call_logs_response(rsps):
    response_body = {
        "items": [
            {"timestamp": 1585925306822, "message": "message 1"},
            {"timestamp": 1585925310822, "message": "message 2"},
        ]
    }
    url = FUNCTIONS_API._get_base_url_with_base_path() + f"/functions/{FUNCTION_ID}/calls/5678/logs"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.GET, url, status=200, json=response_body)

    yield rsps


SCHEDULE1 = {
    "createdTime": 1586944839659,
    "cronExpression": "*/5 * * * *",
    "data": {},
    "description": "Hi",
    "functionExternalId": "user/hello-cognite/hello-cognite:latest",
    "id": 8012683333564363,
    "name": "my-schedule",
    "when": "Every 5 minutes",
}

SCHEDULE2 = {
    "createdTime": 1586944839659,
    "cronExpression": "*/5 * * * *",
    "data": {"value": 2},
    "description": "Hi",
    "functionExternalId": "user/hello-cognite/hello-cognite:latest",
    "id": 8012683333564363,
    "name": "my-schedule",
    "when": "Every 5 minutes",
}


@pytest.fixture
def mock_function_schedules_response(rsps):
    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/schedules"
    rsps.assert_all_requests_are_fired = False
    rsps.add(rsps.GET, url, status=200, json={"items": [SCHEDULE1]})
    rsps.add(rsps.POST, url, status=200, json={"items": [SCHEDULE1]})

    yield rsps


@pytest.fixture
def mock_function_schedules_response_with_data(rsps):
    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/schedules"
    rsps.add(rsps.POST, url, status=200, json={"items": [SCHEDULE2]})

    yield rsps


@pytest.fixture
def mock_function_schedules_delete_response(rsps):
    url = FUNCTIONS_API._get_base_url_with_base_path() + "/functions/schedules/delete"
    rsps.add(rsps.POST, url, status=200, json={})

    yield rsps


class TestFunctionSchedulesAPI:
    def test_list_schedules(self, mock_function_schedules_response):
        res = FUNCTION_SCHEDULES_API.list()
        assert isinstance(res, FunctionSchedulesList)
        expected = mock_function_schedules_response.calls[0].response.json()["items"]
        expected[0].pop("when")
        assert expected == res.dump(camel_case=True)

    def test_create_schedules(self, mock_function_schedules_response):
        res = FUNCTION_SCHEDULES_API.create(
            name="my-schedule",
            function_external_id="user/hello-cognite/hello-cognite:latest",
            cron_expression="*/5 * * * *",
            description="Hi",
        )
        assert isinstance(res, FunctionSchedule)
        expected = mock_function_schedules_response.calls[0].response.json()["items"][0]
        expected.pop("when")
        assert expected == res.dump(camel_case=True)

    def test_create_schedules_with_data(self, mock_function_schedules_response_with_data):
        res = FUNCTION_SCHEDULES_API.create(
            name="my-schedule",
            function_external_id="user/hello-cognite/hello-cognite:latest",
            cron_expression="*/5 * * * *",
            description="Hi",
            data={"value": 2},
        )
        assert isinstance(res, FunctionSchedule)
        expected = mock_function_schedules_response_with_data.calls[0].response.json()["items"][0]
        expected.pop("when")
        assert expected == res.dump(camel_case=True)

    def test_delete_schedules(self, mock_function_schedules_delete_response):
        res = FUNCTION_SCHEDULES_API.delete(id=8012683333564363)
        assert None == res


class TestFunctionCallsAPI:
    def test_list_calls_by_function_id(self, mock_function_calls_list_response):
        res = FUNCTION_CALLS_API.list(function_id=FUNCTION_ID)
        assert isinstance(res, FunctionCallList)
        assert mock_function_calls_list_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_functions_retrieve_response")
    def test_list_calls_by_function_external_id(self, mock_function_calls_list_response):
        res = FUNCTION_CALLS_API.list(function_external_id=f"func-no-{FUNCTION_ID}")
        assert isinstance(res, FunctionCallList)
        assert mock_function_calls_list_response.calls[1].response.json()["items"] == res.dump(camel_case=True)

    def test_retrieve_call_by_function_id(self, mock_function_calls_retrieve_response):
        res = FUNCTION_CALLS_API.retrieve(call_id=5678, function_id=FUNCTION_ID)
        assert isinstance(res, FunctionCall)
        assert mock_function_calls_retrieve_response.calls[0].response.json() == res.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_functions_retrieve_response")
    def test_retrieve_call_by_function_external_id(self, mock_function_calls_retrieve_response):
        res = FUNCTION_CALLS_API.retrieve(call_id=5678, function_external_id=f"func-no-{FUNCTION_ID}")
        assert isinstance(res, FunctionCall)
        assert mock_function_calls_retrieve_response.calls[1].response.json() == res.dump(camel_case=True)

    def test_function_call_logs_by_function_id(self, mock_function_call_logs_response):
        res = FUNCTION_CALLS_API.get_logs(call_id=5678, function_id=FUNCTION_ID)
        assert isinstance(res, FunctionCallLog)
        assert mock_function_call_logs_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_functions_retrieve_response")
    def test_function_call_logs_by_function_external_id(self, mock_function_call_logs_response):
        res = FUNCTION_CALLS_API.get_logs(call_id=5678, function_external_id=f"func-no-{FUNCTION_ID}")
        assert isinstance(res, FunctionCallLog)
        assert mock_function_call_logs_response.calls[1].response.json()["items"] == res.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_function_calls_retrieve_response")
    def test_get_logs_on_retrieved_call_object(self, mock_function_call_logs_response):
        call = FUNCTION_CALLS_API.retrieve(call_id=5678, function_id=FUNCTION_ID)
        logs = call.get_logs()
        assert isinstance(logs, FunctionCallLog)
        assert mock_function_call_logs_response.calls[1].response.json()["items"] == logs.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_function_calls_list_response")
    def test_get_logs_on_listed_call_object(self, mock_function_call_logs_response):
        calls = FUNCTION_CALLS_API.list(function_id=FUNCTION_ID)
        call = calls[0]
        logs = call.get_logs()
        assert isinstance(logs, FunctionCallLog)
        assert mock_function_call_logs_response.calls[1].response.json()["items"] == logs.dump(camel_case=True)

    @pytest.mark.usefixtures("mock_functions_call_completed_response")
    def test_get_logs_on_created_call_object(self, mock_function_call_logs_response):
        call = FUNCTIONS_API.call(id=FUNCTION_ID)
        logs = call.get_logs()
        assert isinstance(logs, FunctionCallLog)
        assert mock_function_call_logs_response.calls[1].response.json()["items"] == logs.dump(camel_case=True)
