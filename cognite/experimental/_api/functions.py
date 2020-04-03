import os
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Union
from zipfile import ZipFile

from cognite.client._api_client import APIClient
from cognite.experimental.data_classes import Function, FunctionList


class FunctionsAPI(APIClient):
    _RESOURCE_PATH = "/functions"

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
        return Function._load(res.json()["items"][0])

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        """Delete one or more functions.s

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
        return FunctionList._load(res.json()["items"])

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
