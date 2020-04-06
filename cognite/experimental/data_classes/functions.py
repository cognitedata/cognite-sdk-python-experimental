from typing import Dict

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
        self._cognite_client = cognite_client

    def call(self, data=None, asynchronous: bool = False):
        return self._cognite_client.functions.call(self.id, data, asynchronous)


class FunctionList(CogniteResourceList):
    _RESOURCE = Function
    _ASSERT_CLASSES = False


class FunctionCall(CogniteResource):
    """A representation of a Cognite Function call.

    Args:
        id (int): A server-generated ID for the object.
        start_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        end_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        response (str): Response from the function. The function must return a JSON serializable object.
        status (str): Status of the function call ("Running" or "Completed").
        error (dict): Error from the function call. It contains an error message and the stack trace.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(
        self,
        id: int = None,
        start_time: int = None,
        end_time: int = None,
        response: str = None,
        status: str = None,
        error: dict = None,
        cognite_client=None,
    ):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.response = response
        self.status = status
        self.error = error
        self._cognite_client = cognite_client
