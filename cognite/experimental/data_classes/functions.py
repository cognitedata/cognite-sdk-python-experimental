from typing import Dict

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class Function(CogniteResource):
    """A representation of a Cognite Function.

    Args:
        name (str): Name of the function.
        description (str): Description of the function.
        status (str): Status of the function.
        filed_id (int): File id of the code represented by this object.
        created_time (int): Created time in UNIX.
        api_key (str): Api key attached to the function.
        secrets (Dict): Secrets attached to the function.
        cognite_client (CogniteClient): An optional CogniteClient to associate with this data class.
    """

    def __init__(
        self,
        name: str = None,
        external_id: str = None,
        description: str = None,
        status: str = None,
        file_id: int = None,
        created_time: int = None,
        api_key: str = None,
        secrets: Dict = None,
        cognite_client=None,
    ):
        self.name = name
        self.external_id = external_id
        self.description = description
        self.status = status
        self.file_id = file_id
        self.created_time = created_time
        self.api_key = api_key
        self.secrets = secrets
        self._cognite_client = cognite_client


class FunctionList(CogniteResourceList):
    _RESOURCE = Function
    _ASSERT_CLASSES = False
