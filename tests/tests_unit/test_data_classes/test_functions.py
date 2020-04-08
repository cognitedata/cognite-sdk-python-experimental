import pytest

from cognite.experimental.data_classes import FunctionCall, FunctionCallList

CALL_RESPONSE = {"id": 5678, "startTime": 1585925306822, "endTime": 1585925310822, "status": "Completed"}


class TestFunctionCall:
    def test_load(self):
        function_id = 1234
        call = FunctionCall._load(CALL_RESPONSE, function_id=function_id)
        assert function_id == call._function_id
        assert CALL_RESPONSE == call.dump(camel_case=True)


class TestFunctionCallList:
    def test_load(self):
        function_id = 1234
        calls = FunctionCallList._load([CALL_RESPONSE], function_id=function_id)
        assert function_id == calls[0]._function_id
        assert [CALL_RESPONSE] == calls.dump(camel_case=True)
