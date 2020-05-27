from cognite.experimental.data_classes import FunctionCall, FunctionCallList

CALL_RESPONSE = {
    "id": 5678,
    "startTime": 1585925306822,
    "endTime": 1585925310822,
    "status": "Completed",
    "functionId": 1234,
}


class TestFunctionCall:
    def test_load(self):

        call = FunctionCall._load(CALL_RESPONSE)
        assert CALL_RESPONSE == call.dump(camel_case=True)


class TestFunctionCallList:
    def test_load(self):

        calls = FunctionCallList._load([CALL_RESPONSE])
        assert [CALL_RESPONSE] == calls.dump(camel_case=True)
