import os
from inspect import getsource
from tempfile import TemporaryDirectory
from typing import Any, Callable, Dict, List, Optional, Union
from zipfile import ZipFile

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.experimental.data_classes import Function, FunctionCall, FunctionCallList, FunctionCallLog, FunctionList


class FunctionsAPI(APIClient):
    _RESOURCE_PATH = "/functions"
    _LIST_CLASS = FunctionList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls = FunctionCallsAPI(*args, **kwargs)

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
            filde_id (int, optional):               File ID of the code uploaded to the Files API.
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
            file_id = self._zip_and_upload_folder(folder, name)
        elif function_handle:
            self._validate_function_handle(function_handle)
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
        asynchronous: bool = False,
    ) -> FunctionCall:
        """Call a function by its ID or external ID. Can be done `synchronously <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-function_name-call>`_ or `asynchronously <https://docs.cognite.com/api/playground/#operation/post-api-playground-projects-project-functions-functionId-async_call>`_.

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID
            data (Union[str, dict], optional): Input data to the function (JSON serializable). This data is passed deserialized into the function through one of the arguments called data.
            asynchronous (bool): Call the function asynchronously. Defaults to false.

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

        url = f"/functions/{id}/call" if not asynchronous else f"/functions/{id}/async_call"
        body = {}
        if data:
            body = {"data": data}
        res = self._post(url, json=body)
        return FunctionCall._load(res.json(), function_id=id, cognite_client=self._cognite_client)

    def _zip_and_upload_folder(self, folder, name) -> int:
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
        with TemporaryDirectory() as tmpdir:
            handle_path = os.path.join(tmpdir, "handler.py")
            with open(handle_path, "w") as f:
                source = getsource(function_handle)
                f.write(source)

            zip_path = os.path.join(tmpdir, "function.zip")
            zf = ZipFile(zip_path, "w")
            zf.write(handle_path, arcname="handler.py")
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

    @staticmethod
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
    def list(self, function_id: Optional[int] = None, function_external_id: Optional[str] = None) -> FunctionCallList:
        """`List all calls associated with a specific function. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name-calls>`_

        Args:
            function_id (int, optional): ID of the function on which the calls were made.
            external_id (str, optional): External ID of the function on which the calls were made.

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
        url = f"/functions/{function_id}/calls"
        res = self._get(url)
        return FunctionCallList._load(res.json()["items"], function_id=function_id, cognite_client=self._cognite_client)

    def retrieve(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCall:
        """`Retrieve call by id. <https://docs.cognite.com/api/playground/#operation/get-api-playground-projects-project-functions-function_name-calls-call_id>`_

        Args:
            call_id (int): ID of the call.
            function_id (int, optional): ID of the function on which the call was made.
            external_id (str, optional): External ID of the function on which the call was made.

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
        return FunctionCall._load(res.json(), function_id=function_id, cognite_client=self._cognite_client)

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
