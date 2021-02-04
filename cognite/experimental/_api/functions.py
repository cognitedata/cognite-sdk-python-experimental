import importlib.util
import json
import os
import sys
import time
from inspect import getsource
from numbers import Number
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Dict, List, Optional, Union
from zipfile import ZipFile

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    Function,
    FunctionCall,
    FunctionCallList,
    FunctionCallLog,
    FunctionList,
    FunctionSchedule,
    FunctionSchedulesList,
)


class FunctionsAPI(APIClient):
    _RESOURCE_PATH = "/functions"
    _LIST_CLASS = FunctionList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls = FunctionCallsAPI(*args, **kwargs)
        self.schedules = FunctionSchedulesAPI(*args, **kwargs)

    def create(
        self,
        name: str,
        folder: Optional[str] = None,
        file_id: Optional[int] = None,
        function_path: Optional[str] = HANDLER_FILE_NAME,
        function_handle: Optional[Callable] = None,
        external_id: Optional[str] = None,
        description: Optional[str] = "",
        owner: Optional[str] = "",
        api_key: Optional[str] = None,
        secrets: Optional[Dict] = None,
        env_vars: Optional[Dict] = None,
        cpu: Number = 0.25,
        memory: Number = 1.0,
    ) -> Function:
        """`When creating a function, <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions>`_
        the source code can be specified in one of three ways:\n
        - Via the `folder` argument, which is the path to the folder where the source code is located. `function_path` must point to a python file in the folder within which a function named `handle` must be defined.\n
        - Via the `file_id` argument, which is the ID of a zip-file uploaded to the files API. `function_path` must point to a python file in the zipped folder within which a function named `handle` must be defined.\n
        - Via the `function_handle` argument, which is a reference to a function object, which must be named `handle`.\n

        The function named `handle` is the entrypoint of the created function. Valid arguments to `handle` are `data`, `client`, `secrets` and `function_call_info`:\n
        - If the user calls the function with input data, this is passed through the `data` argument.\n
        - If the user gives an `api_key` when creating the function, a pre instantiated CogniteClient is passed through the `client` argument.\n
        - If the user gives one ore more secrets when creating the function, these are passed through the `secrets` argument. The API key can be access through `secrets["apikey"]`.\n
        - Data about the function call can be accessed via the argument `function_call_info`, which is a dictionary with keys `function_id` and, if the call is scheduled, `schedule_id` and `scheduled_time`.\n

        Args:
            name (str):                             The name of the function.
            folder (str, optional):                 Path to the folder where the function source code is located.
            file_id (int, optional):                File ID of the code uploaded to the Files API.
            function_path (str, optional):          Relative path from the root folder to the file containing the `handle` function. Defaults to `handler.py`. Must be on POSIX path format.
            function_handle (Callable, optional):   Reference to a function object, which must be named `handle`.
            external_id (str, optional):            External id of the function.
            description (str, optional):            Description of the function.
            owner (str, optional):                  Owner of this function. Typically used to know who created it.
            api_key (str, optional):                API key that can be used inside the function to access data in CDF.
            secrets (Dict[str, str]):               Additional secrets as key/value pairs. These can e.g. password to simulators or other data sources. Keys must be lowercase characters, numbers or dashes (-) and at most 15 characters. You can create at most 5 secrets, all keys must be unique, and cannot be apikey.
            env_vars (Dict[str, str]):              Environment variables as key/value pairs. Keys can contain only letters, numbers or the underscore character. You can create at most 20 environment variables.
            cpu (Number):                           Number of CPU cores per function. Defaults to 0.25. Allowed values are in the range [0.1, 0.6].
            memory (Number):                        Memory per function measured in GB. Defaults to 1. Allowed values are in the range [0.1, 2.5].

        Returns:
            Function: The created function.

        Examples:

            Create function with source code in folder::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", folder="path/to/code", function_path="path/to/function.py")

            Create function with file_id from already uploaded source code::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", file_id=123, function_path="path/to/function.py")

            Create function with predefined function object named `handle`::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", function_handle=handle)
        """
        self._assert_exactly_one_of_folder_or_file_id_or_function_handle(folder, file_id, function_handle)

        if folder:
            validate_function_folder(folder, function_path)
            file_id = self._zip_and_upload_folder(folder, name)
        elif function_handle:
            _validate_function_handle(function_handle)
            file_id = self._zip_and_upload_handle(function_handle, name)
        utils._auxiliary.assert_type(cpu, "cpu", [Number], allow_none=False)
        utils._auxiliary.assert_type(memory, "memory", [Number], allow_none=False)

        sleep_time = 1.0  # seconds
        for i in range(MAX_RETRIES):
            file = self._cognite_client.files.retrieve(id=file_id)
            if file is None or not file.uploaded:
                time.sleep(sleep_time)
                sleep_time *= 2
            else:
                break
        else:
            raise IOError("Could not retrieve file from files API")

        url = "/functions"
        function = {
            "name": name,
            "description": description,
            "owner": owner,
            "fileId": file_id,
            "functionPath": function_path,
            "cpu": float(cpu),
            "memory": float(memory),
            "envVars": env_vars,
        }
        if external_id:
            function.update({"externalId": external_id})
        if api_key:
            function.update({"apiKey": api_key})
        if secrets:
            function.update({"secrets": secrets})
        body = {"items": [function]}
        res = self._post(url, json=body)
        return Function._load(res.json()["items"][0], cognite_client=self._cognite_client)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        """`Delete one or more functions. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-delete>`_

        Args:
            id (Union[int, List[int]): Id or list of ids.
            external_id (Union[str, List[str]]): External ID or list of external ids.

        Returns:
            None

        Example:

            Delete functions by id or external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.functions.delete(id=[1,2,3], external_id="function3")
        """
        self._delete_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def list(self, limit: Optional[int] = LIST_LIMIT_DEFAULT) -> FunctionList:
        """`List all functions. <https://docs.cognite.com/api/playground/#operation/get-function>`_

        Args:
            limit (int, optional): Maximum number of functions to list. Pass in -1, float('inf') or None to list all functions.

        Returns:
            FunctionList: List of functions

        Example:

            List functions::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> functions_list = c.functions.list()
        """
        url = "/functions"

        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        params = {"limit": limit}
        res = self._get(url, params=params)
        return FunctionList._load(res.json()["items"], cognite_client=self._cognite_client)

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[Function]:
        """`Retrieve a single function by id. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-context-functions-byids>`_

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID

        Returns:
            Optional[Function]: Requested function or None if it does not exist.

        Examples:

            Get function by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.functions.retrieve(id=1)

            Get function by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.functions.retrieve(external_id="1")
        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def retrieve_multiple(
        self, ids: Optional[List[int]] = None, external_ids: Optional[List[str]] = None
    ) -> FunctionList:
        """`Retrieve multiple functions by id. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-context-functions-byids>`_

        Args:
            ids (List[int], optional): IDs
            external_ids (List[str], optional): External IDs

        Returns:
            FunctionList: The requested functions.

        Examples:

            Get function by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.functions.retrieve_multiple(ids=[1, 2, 3])

            Get functions by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.functions.retrieve_multiple(external_ids=["func1", "func2"])
        """
        utils._auxiliary.assert_type(ids, "id", [List], allow_none=True)
        utils._auxiliary.assert_type(external_ids, "external_id", [List], allow_none=True)
        return self._retrieve_multiple(ids=ids, external_ids=external_ids, wrap_ids=True)

    def call(
        self,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        data: Optional[Dict] = None,
        wait: bool = True,
    ) -> FunctionCall:
        """Call a function by its ID or external ID. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-function_name-call>`_.

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID
            data (Union[str, dict], optional): Input data to the function (JSON serializable). This data is passed deserialized into the function through one of the arguments called data.
            wait (bool): Wait until the function call is finished. Defaults to True.

        Returns:
            FunctionCall: A function call object.

        Examples:

            Call a function by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> call = c.functions.call(id=1)

            Call a function directly on the `Function` object::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> func = c.functions.retrieve(id=1)
                >>> call = func.call()
        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        if external_id:
            id = self.retrieve(external_id=external_id).id

        url = f"/functions/{id}/call"
        body = {}
        if data:
            body = {"data": data}
        res = self._post(url, json=body)

        function_call = FunctionCall._load(res.json(), cognite_client=self._cognite_client)
        if wait:
            function_call.wait()

        return function_call

    def _zip_and_upload_folder(self, folder, name) -> int:
        # / is not allowed in file names
        name = name.replace("/", "-")

        current_dir = os.getcwd()
        os.chdir(folder)

        try:
            with TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, "function.zip")
                zf = ZipFile(zip_path, "w")
                for root, dirs, files in os.walk("."):
                    zf.write(root)
                    for filename in files:
                        zf.write(os.path.join(root, filename))
                zf.close()

                file = self._cognite_client.files.upload(zip_path, name=f"{name}.zip")

            return file.id

        finally:
            os.chdir(current_dir)

    def _zip_and_upload_handle(self, function_handle, name) -> int:
        # / is not allowed in file names
        name = name.replace("/", "-")

        with TemporaryDirectory() as tmpdir:
            handle_path = os.path.join(tmpdir, HANDLER_FILE_NAME)
            with open(handle_path, "w") as f:
                source = getsource(function_handle)
                f.write(source)

            zip_path = os.path.join(tmpdir, "function.zip")
            zf = ZipFile(zip_path, "w")
            zf.write(handle_path, arcname=HANDLER_FILE_NAME)
            zf.close()

            file = self._cognite_client.files.upload(zip_path, name=f"{name}.zip")

        return file.id

    @staticmethod
    def _assert_exactly_one_of_folder_or_file_id_or_function_handle(folder, file_id, function_handle):
        source_code_options = {"folder": folder, "file_id": file_id, "function_handle": function_handle}
        given_source_code_options = [key for key in source_code_options.keys() if source_code_options[key]]
        if len(given_source_code_options) < 1:
            raise TypeError("Exactly one of the arguments folder, file_id and handle is required, but none were given.")
        elif len(given_source_code_options) > 1:
            raise TypeError(
                "Exactly one of the arguments folder, file_id and handle is required, but "
                + ", ".join(given_source_code_options)
                + " were given."
            )


def convert_file_path_to_module_path(file_path: str):
    return ".".join(Path(file_path).with_suffix("").parts)


def validate_function_folder(root_path, function_path):
    file_extension = Path(function_path).suffix
    if file_extension != ".py":
        raise TypeError(f"{function_path} is not a valid value for function_path. File extension must be .py.")

    function_path_full = Path(root_path) / Path(
        function_path
    )  # This converts function_path to a Windows path if running on Windows
    if not function_path_full.is_file():
        raise TypeError(f"No file found at location '{function_path}' in '{root_path}'.")

    sys.path.insert(0, root_path)

    # Necessary to clear the cache if you have previously imported the module (this would have precedence over sys.path)
    cached_handler_module = sys.modules.get("handler")
    if cached_handler_module:
        del sys.modules["handler"]

    module_path = convert_file_path_to_module_path(function_path)
    handler = importlib.import_module(module_path)

    if "handle" not in handler.__dir__():
        raise TypeError(f"{function_path} must contain a function named 'handle'.")

    _validate_function_handle(handler.handle)
    sys.path.remove(root_path)


def _validate_function_handle(function_handle):
    if not function_handle.__code__.co_name == "handle":
        raise TypeError("Function referenced by function_handle must be named handle.")
    if not set(function_handle.__code__.co_varnames[: function_handle.__code__.co_argcount]).issubset(
        set(["data", "client", "secrets", "function_call_info"])
    ):
        raise TypeError(
            "Arguments to function referenced by function_handle must be a subset of (data, client, secrets, function_call_info)"
        )


class FunctionCallsAPI(APIClient):
    _LIST_CLASS = FunctionCallList

    def list(
        self,
        function_id: Optional[int] = None,
        function_external_id: Optional[str] = None,
        status: Optional[str] = None,
        schedule_id: Optional[int] = None,
        start_time: Optional[Dict[str, int]] = None,
        end_time: Optional[Dict[str, int]] = None,
        limit: Optional[int] = LIST_LIMIT_DEFAULT,
    ) -> FunctionCallList:
        """List all calls associated with a specific function id. Either function_id or function_external_id must be specified.

        Args:
            function_id (int, optional): ID of the function on which the calls were made.
            function_external_id (str, optional): External ID of the function on which the calls were made.
            status (str, optional): Status of the call. Possible values ["Running", "Failed", "Completed", "Timeout"].
            schedule_id (int, optional): Schedule id from which the call belongs (if any).
            start_time (Dict[str, int], optional): Start time of the call. Possible keys are `min` and `max`, with values given as time stamps in ms.
            end_time (Dict[str, int], optional): End time of the call. Possible keys are `min` and `max`, with values given as time stamps in ms.
            limit (int, optional): Maximum number of function calls to list. Pass in -1, float('inf') or None to list all Function Calls.

        Returns:
            FunctionCallList: List of function calls

        Examples:

            List function calls::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> calls = c.functions.calls.list(function_id=1)

            List function calls directly on a function object::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> func = c.functions.retrieve(id=1)
                >>> calls = func.list_calls()

        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(function_id, function_external_id)
        if function_external_id:
            function_id = self._cognite_client.functions.retrieve(external_id=function_external_id).id
        filter = {"status": status, "scheduleId": schedule_id, "startTime": start_time, "endTime": end_time}
        resource_path = f"/functions/{function_id}/calls"

        return self._list(method="POST", resource_path=resource_path, filter=filter, limit=limit)

    def retrieve(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> Optional[FunctionCall]:
        """`Retrieve a single function call by id. <https://docs.cognite.com/api/playground/#operation/byidsFunctionCalls>`_

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            function_external_id (str, optional): External ID of the function on which the call was made.

        Returns:
            Optional[FunctionCall]: Requested function call.

        Examples:

            Retrieve single function call by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> call = c.functions.calls.retrieve(call_id=2, function_id=1)

            Retrieve function call directly on a function object::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> func = c.functions.retrieve(id=1)
                >>> call = func.retrieve_call(id=2)

        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(function_id, function_external_id)
        if function_external_id:
            function_id = self._cognite_client.functions.retrieve(external_id=function_external_id).id
        resource_path = f"/functions/{function_id}/calls"
        return self._retrieve_multiple(wrap_ids=True, resource_path=resource_path, ids=call_id)

    def get_response(self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None):
        """Retrieve the response from a function call.

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            function_external_id (str, optional): External ID of the function on which the call was made.

        Returns:
            Response from the function call.

        Examples:

            Retrieve function call response by call ID::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> response = c.functions.calls.get_response(call_id=2, function_id=1)

            Retrieve function call response directly on a call object::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> call = c.functions.calls.retrieve(call_id=2, function_id=1)
                >>> response = call.get_response()

        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(function_id, function_external_id)
        if function_external_id:
            function_id = self._cognite_client.functions.retrieve(external_id=function_external_id).id
        url = f"/functions/{function_id}/calls/{call_id}/response"
        res = self._get(url)
        return res.json().get("response")

    def get_logs(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCallLog:
        """`Retrieve logs for function call. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name-calls>`_

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            function_external_id (str, optional): External ID of the function on which the call was made.

        Returns:
            FunctionCallLog: Log for the function call.

        Examples:

            Retrieve function call logs by call ID::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> logs = c.functions.calls.get_logs(call_id=2, function_id=1)

            Retrieve function call logs directly on a call object::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> call = c.functions.calls.retrieve(call_id=2, function_id=1)
                >>> logs = call.get_logs()

        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(function_id, function_external_id)
        if function_external_id:
            function_id = self._cognite_client.functions.retrieve(external_id=function_external_id).id
        url = f"/functions/{function_id}/calls/{call_id}/logs"
        res = self._get(url)
        return FunctionCallLog._load(res.json()["items"])


class FunctionSchedulesAPI(APIClient):
    _RESOURCE_PATH = "/functions/schedules"
    _LIST_CLASS = FunctionSchedulesList

    def retrieve(self, id: int) -> Optional[FunctionSchedule]:
        """`Retrieve a single function schedule by id. <https://docs.cognite.com/api/playground/#operation/byidsFunctionSchedules>`_

        Args:
            id (int): ID

        Returns:
            Optional[FunctionSchedule]: Requested function schedule.


        Examples:

            Get function schedule by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.functions.schedules.retrieve(id=1)

        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id=id, external_id=None)
        return self._retrieve_multiple(ids=id, wrap_ids=True)

    def list(self, limit: Optional[int] = LIST_LIMIT_DEFAULT) -> FunctionSchedulesList:
        """`List all schedules associated with a specific project. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-schedules>`_

        Args:
            limit (int, optional): Maximum number of schedules to list. Pass in -1, float('inf') or None to list all schedules.

        Returns:
            FunctionSchedulesList: List of function schedules

        Examples:

            List function schedules::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> schedules = c.functions.schedules.list()

            List schedules directly on a function object to get only schedules associated with this particular function:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> func = c.functions.retrieve(id=1)
                >>> schedules = func.list_schedules()

        """
        url = f"/functions/schedules"

        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        params = {"limit": limit}
        res = self._get(url, params=params)
        return FunctionSchedulesList._load(res.json()["items"])

    def create(
        self,
        name: str,
        function_external_id: str,
        cron_expression: str,
        description: str = "",
        data: Optional[Dict] = None,
    ) -> FunctionSchedule:
        """`Create a schedule associated with a specific project. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-schedules>`_

        Args:
            name (str): Name of the schedule.
            function_external_id (str): External id of the function.
            description (str): Description of the schedule.
            cron_expression (str): Cron expression.
            data (optional, Dict): Data to be passed to the scheduled run.

        Returns:
            FunctionSchedule: Created function schedule.

        Examples:

            Create function schedule::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> schedule = c.functions.schedules.create(
                    name= "My schedule",
                    function_external_id="my-external-id",
                    cron_expression="*/5 * * * *",
                    description="This schedule does magic stuff.")

        """
        json = {
            "items": [
                {
                    "name": name,
                    "description": description,
                    "functionExternalId": function_external_id,
                    "cronExpression": cron_expression,
                }
            ]
        }
        if data:
            json["items"][0]["data"] = data

        url = f"/functions/schedules"
        res = self._post(url, json=json)
        return FunctionSchedule._load(res.json()["items"][0])

    def delete(self, id: int) -> None:
        """`Delete a schedule associated with a specific project. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-schedules-delete>`_

        Args:
            id (int): Id of the schedule

        Returns:
            None

        Examples:

            Delete function schedule::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.functions.schedules.delete(id = 123)

        """
        json = {"items": [{"id": id,}]}
        url = f"/functions/schedules/delete"
        self._post(url, json=json)

    def get_input_data(self, id: int) -> Dict:
        """
        Retrieve the input data to the associated function.
        Args:
            id (int): Id of the schedule

        Returns:
            Input data to the associated function. This data is passed
            deserialized into the function through the data argument.
        Examples:

            Get schedule input data::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.functions.schedules.get_input_data(id = 123)
        """
        url = f"/functions/schedules/{id}/input_data"
        res = self._get(url)

        return res.json()["data"]
