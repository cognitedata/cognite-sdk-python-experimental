import os
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional, Union
from zipfile import ZipFile

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.experimental.data_classes import Function, FunctionCall, FunctionCallList, FunctionList


class FunctionsAPI(APIClient):
    _RESOURCE_PATH = "/functions"
    _LIST_CLASS = FunctionList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls = FunctionCallsAPI(*args, **kwargs)

    def create(
        self,
        name: str,
        folder: str = None,
        file_id: int = None,
        external_id: str = None,
        description: str = "",
        owner: str = "",
        api_key: str = None,
        secrets: Dict = None,
    ) -> Function:
        """Creates a new function from source code located in folder

        Args:
            name (str):                 Name of function
            folder (str):               Path to folder where the function source code is located
            external_id (str):          External id of the function
            description (str):          Description of the function
            owner (str):                Owner of the function
            api_key (str):              Api key to be used by the CogniteClient in the function source code
            secrets (Dict[str, str]):   Secrets attached to the function ((key, value) pairs)

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
        """
        if folder and file_id:
            raise TypeError("Exactly one of the arguments `path` and `file_id` is required, but both were given.")
        if not folder and not file_id:
            raise TypeError("Exactly one of the arguments `path` and `file_id` is required, but none were given.")

        if not file_id:
            file_id = self._zip_and_upload_folder(folder, name)

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
        """Delete one or more functions.

        Args:
            id (Union[int, List[int]): Id or list of ids
            external_id (Union[str, List[str]]): External ID or list of external ids

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
        """List all functions.

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
        """Retrieve a single function by id.

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
        """Retrieve multiple functions by id.

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

    def call(self, id: int = None, external_id: str = None, data=None, asynchronous: bool = False) -> FunctionCall:
        """Call a function by its ID or external ID.

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID
            data (optional): Input data to the function (JSON serializable). This data is passed deserialized into the function through one of the arguments called data.
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
        return FunctionCall._load(res.json())

    def _zip_and_upload_folder(self, folder, name) -> int:
        current_dir = os.getcwd()
        os.chdir(folder)

        with TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "function.zip")
            zf = ZipFile(zip_path, "w")
            for root, dirs, files in os.walk("."):
                zf.write(root)
                for filename in files:
                    zf.write(os.path.join(root, filename))
            zf.close()

            file = self._cognite_client.files.upload(zip_path, name=f"{name}.zip")

        os.chdir(current_dir)

        return file.id


class FunctionCallsAPI(APIClient):
    def list(self, function_id: Optional[int] = None, function_external_id: Optional[str] = None) -> FunctionCallList:
        """List all calls associated with a specific function.

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
        return FunctionCallList._load(res.json()["items"], cognite_client=self._cognite_client)

    def retrieve(
        self, call_id: int, function_id: Optional[int] = None, function_external_id: Optional[str] = None
    ) -> FunctionCall:
        """Retrieve call by id.

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
        url = f"/functions/{function_id}/calls/{call_id}"
        if function_external_id:
            id = self.retrieve(external_id=external_id).id
        res = self._get(url)
        return FunctionCall._load(res.json(), cognite_client=self._cognite_client)
