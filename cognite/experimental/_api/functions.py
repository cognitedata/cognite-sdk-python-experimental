import os
import sys
from inspect import getsource
from tempfile import TemporaryDirectory
from typing import Any, Callable, Dict, List, Optional, Union
from zipfile import ZipFile

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.experimental.data_classes import (
    Function,
    FunctionCall,
    FunctionCallList,
    FunctionCallLog,
    FunctionCallResponse,
    FunctionList,
    FunctionSchedule,
    FunctionSchedulesList,
)

HANDLER_FILE_NAME = "handler.py"


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
        function_handle: Optional[Callable] = None,
        external_id: Optional[str] = None,
        description: Optional[str] = "",
        owner: Optional[str] = "",
        api_key: Optional[str] = None,
        secrets: Optional[Dict] = None,
    ) -> Function:
        """`Create a new function from source code located in folder. <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions>`_

        Args:
            name (str):                             The name of the function.
            folder (str, optional):                 Path to the folder where the function source code is located.
            file_id (int, optional):                File ID of the code uploaded to the Files API.
            function_handle (Callable, optional):   Reference to a function object, which must be named `handle`. Valid arguments to `handle` are `data`, `client` and `secret`.
            external_id (str, optional):            External id of the function.
            description (str, optional):            Description of the function.
            owner (str, optional):                  Owner of this function. Typically used to know who created it.
            api_key (str, optional):                API key that can be used inside the function to access data in CDF.
            secrets (Dict[str, str]):               Additional secrets as key/value pairs. These can e.g. password to simulators or other data sources. Keys must be lowercase characters, numbers or dashes (-) and at most 15 characters. You can create at most 5 secrets, all keys must be unique, and cannot be apikey.

        Returns:
            Function: The created function.

        Examples:

            Create function with source code in folder::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", folder="path/to/code")

            Create function with file_id from already uploaded source code::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", file_id=123)

            Create function with predefined function object named `handle`::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> function = c.functions.create(name="myfunction", function_handle=handle)
        """
        self._assert_exactly_one_of_folder_or_file_id_or_function_handle(folder, file_id, function_handle)

        if folder:
            validate_function_folder(folder)
            file_id = self._zip_and_upload_folder(folder, name)
        elif function_handle:
            _validate_function_handle(function_handle)
            file_id = self._zip_and_upload_handle(function_handle, name)

        url = "/functions"
        function = {"name": name, "description": description, "owner": owner, "fileId": file_id}
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

    def list(self) -> FunctionList:
        """`List all functions. <https://docs.cognite.com/api/playground/#operation/get-function>`_

        Returns:
            FunctionList: List of functions

        Example:

            List functions::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> functions_list = c.functions.list()
        """
        url = "/functions"
        res = self._get(url)
        return FunctionList._load(res.json()["items"], cognite_client=self._cognite_client)

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[Function]:
        """`Retrieve a single function by id. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name>`_

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


def validate_function_folder(path):
    sys.path.insert(0, path)
    if HANDLER_FILE_NAME not in os.listdir(path):
        sys.path.remove(path)
        raise TypeError(f"Function folder must contain a module named {HANDLER_FILE_NAME}.")

    cached_handler_module = sys.modules.get("handler")
    if cached_handler_module:
        del sys.modules["handler"]
    import handler

    if "handle" not in handler.__dir__():
        sys.path.remove(path)
        raise TypeError(f"{HANDLER_FILE_NAME} must contain a function named 'handle'.")

    _validate_function_handle(handler.handle)
    sys.path.remove(path)
    if cached_handler_module:
        sys.modules["handler"] = cached_handler_module


def _validate_function_handle(function_handle):
    if not function_handle.__code__.co_name == "handle":
        raise TypeError("Function referenced by function_handle must be named handle.")
    if not set(function_handle.__code__.co_varnames[: function_handle.__code__.co_argcount]).issubset(
        set(["data", "client", "secrets"])
    ):
        raise TypeError(
            "Arguments to function referenced by function_handle must be a subset of (data, client, secrets)"
        )


class FunctionCallsAPI(APIClient):
    def list(
        self,
        function_id: Optional[int] = None,
        function_external_id: Optional[str] = None,
        status: Optional[str] = None,
        schedule_id: Optional[int] = None,
        start_time: Optional[Dict[str, int]] = None,
        end_time: Optional[Dict[str, int]] = None,
    ) -> FunctionCallList:
        """List all calls associated with a specific function id. Either function_id or function_external_id must be specified.

        Args:
            function_id (int, optional): ID of the function on which the calls were made.
            status (str, optional): Status of the call. Possible values ["Running", "Failed", "Completed", "Timeout"].
            schedule_id (int, optional): Schedule id from which the call belongs (if any).
            start_time (Union[Dict[str, int], TimestampRange]): Start time of the call. Possible keys are `min` and `max`, with values given as time stamps in ms.
            end_time (Union[Dict[str, int], TimestampRange]): End time of the call. Possible keys are `min` and `max`, with values given as time stamps in ms.
            function_external_id (str, optional): External ID of the function on which the calls were made.

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
        url = f"/functions/{function_id}/calls/list"
        filter = {"status": status, "scheduleId": schedule_id, "startTime": start_time, "endTime": end_time}
        post_body = {"filter": filter}
        res = self._post(url, json=post_body)
        return FunctionCallList._load(res.json()["items"], cognite_client=self._cognite_client)

    def retrieve(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCall:
        """`Retrieve call by id. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name-calls-call_id>`_

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            function_external_id (str, optional): External ID of the function on which the call was made.

        Returns:
            FunctionCall: Function call.

        Examples:

            Retrieve function call by id::

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
        url = f"/functions/{function_id}/calls/{call_id}"
        res = self._get(url)
        return FunctionCall._load(res.json(), cognite_client=self._cognite_client)

    def get_response(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCallResponse:
        """Retrieve the response from a function call.

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            function_external_id (str, optional): External ID of the function on which the call was made.

        Returns:
            FunctionCallResponse: Response from the function call.

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
        return FunctionCallResponse._load(res.json())

    def get_logs(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCallLog:
        """`Retrieve logs for function call. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name-calls>`_

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            external_id (str, optional): External ID of the function on which the call was made.

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
    def list(self) -> FunctionSchedulesList:
        """`List all schedules associated with a specific project. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-schedules>`_

        Returns:
            FunctionSchedulesList: List of function schedules

        Examples:

            List function schedules::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> schedules = c.functions.schedules.list()

        """
        url = f"/functions/schedules"
        res = self._get(url)
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
