import time
from typing import Dict, List, Optional, Union

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class Function(CogniteResource):
    """A representation of a Cognite Function.

    Args:
        id (int): Id of the function.
        name (str): Name of the function.
        external_id (str): External id of the function.
        description (str): Description of the function.
        owner (str): Owner of the function.
        status (str): Status of the function.
        filed_id (int): File id of the code represented by this object.
        created_time (int): Created time in UNIX.
        api_key (str): Api key attached to the function.
        secrets (Dict[str, str]): Secrets attached to the function ((key, value) pairs).
        error(Dict[str, str]): Dictionary with keys "message" and "trace", which is populated if deployment fails.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(
        self,
        id: int = None,
        name: str = None,
        external_id: str = None,
        description: str = None,
        owner: str = None,
        status: str = None,
        file_id: int = None,
        created_time: int = None,
        api_key: str = None,
        secrets: Dict = None,
        error: Dict = None,
        cognite_client=None,
    ):
        self.id = id
        self.name = name
        self.external_id = external_id
        self.description = description
        self.owner = owner
        self.status = status
        self.file_id = file_id
        self.created_time = created_time
        self.api_key = api_key
        self.secrets = secrets
        self.error = error
        self._cognite_client = cognite_client

    def call(self, data=None, wait: bool = True):
        return self._cognite_client.functions.call(id=self.id, data=data, wait=wait)

    def list_calls(
        self,
        status: Optional[str] = None,
        schedule_id: Optional[int] = None,
        start_time: Optional[Dict[str, int]] = None,
        end_time: Optional[Dict[str, int]] = None,
    ):
        return self._cognite_client.functions.calls.list(
            function_id=self.id, status=status, schedule_id=schedule_id, start_time=start_time, end_time=end_time
        )

    def list_schedules(self):
        all_schedules = self._cognite_client.functions.schedules.list()
        function_schedules = filter(lambda f: f.function_external_id == self.external_id, all_schedules)
        return list(function_schedules)

    def retrieve_call(self, id: int):
        return self._cognite_client.functions.calls.retrieve(call_id=id, function_id=self.id)


class FunctionSchedule(CogniteResource):
    """A representation of a Cognite Function Schedule.

    Args:
        id (int): Id of the schedule.
        name (str): Name of the function schedule.
        function_external_id (str): External id of the function.
        description (str): Description of the function schedule.
        cron_expression (str): Cron expression
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        data (Dict): Data to be passed to the scheduled run.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(
        self,
        id: int = None,
        name: str = None,
        function_external_id: str = None,
        description: str = None,
        created_time: int = None,
        cron_expression: str = None,
        data: Dict = None,
        cognite_client=None,
    ):
        self.id = id
        self.name = name
        self.function_external_id = function_external_id
        self.description = description
        self.cron_expression = cron_expression
        self.created_time = created_time
        self.data = data
        self._cognite_client = cognite_client


class FunctionSchedulesList(CogniteResourceList):
    _RESOURCE = FunctionSchedule
    _ASSERT_CLASSES = False


class FunctionList(CogniteResourceList):
    _RESOURCE = Function
    _ASSERT_CLASSES = False


class FunctionCall(CogniteResource):
    """A representation of a Cognite Function call.

    Args:
        id (int): A server-generated ID for the object.
        start_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        end_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        status (str): Status of the function call ("Running" or "Completed").
        schedule_id (int): The schedule id belonging to the call.
        error (dict): Error from the function call. It contains an error message and the stack trace.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(
        self,
        id: int = None,
        start_time: int = None,
        end_time: int = None,
        status: str = None,
        schedule_id: int = None,
        error: dict = None,
        function_id: int = None,
        cognite_client=None,
    ):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.schedule_id = schedule_id
        self.error = error
        self.function_id = function_id
        self._cognite_client = cognite_client

    def get_response(self):
        return self._cognite_client.functions.calls.get_response(call_id=self.id, function_id=self.function_id)

    def get_logs(self):
        return self._cognite_client.functions.calls.get_logs(call_id=self.id, function_id=self.function_id)

    def update(self):
        latest = self._cognite_client.functions.calls.retrieve(call_id=self.id, function_id=self.function_id)
        self.status = latest.status
        self.end_time = latest.end_time
        self.error = latest.error

    def wait(self):
        while self.status == "Running":
            self.update()
            time.sleep(1.0)


class FunctionCallList(CogniteResourceList):
    _RESOURCE = FunctionCall
    _ASSERT_CLASSES = False


class FunctionCallResponse(CogniteResource):
    """The response from a function call.

    Args:
        function_id (int): The ID of the function on which the call was made.
        call_id (int): The ID of the call.
        response (str): The function call response.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(self, call_id: int = None, function_id: int = None, response: str = None, cognite_client=None):
        self.call_id = call_id
        self.function_id = function_id
        self.response = response
        self._cognite_client = cognite_client


class FunctionCallLogEntry(CogniteResource):
    """A log entry for a function call.

    Args:
        timestamp (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        message (str): Single line from stdout / stderr.
    """

    def __init__(self, timestamp: int = None, message: str = None, cognite_client=None):
        self.timestamp = timestamp
        self.message = message
        self._cognite_client = cognite_client


class FunctionCallLog(CogniteResourceList):
    _RESOURCE = FunctionCallLogEntry
    _ASSERT_CLASSES = False
