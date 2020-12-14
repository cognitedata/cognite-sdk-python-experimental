from cognite.client.data_classes._base import *


class Integration(CogniteResource):
    """A representation of an integration.

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
        name (str): The name of the integration.
        description (str): The description of the integration.
        data_set_id (int): The id of the dataset this integration related with.
        last_success (int): Milliseconds value of last success status.
        last_failure (int): Milliseconds value of last failure status.
        last_seen (int): Milliseconds value of last seen status.
        schedule (str): undefined/triggered/streamed/cron regex.
        owner (dict[str, Any]): owner record in dict format: {"name": "value", "email": "value"}.
        authors (List[Dict[str, Any]]): list of responsible users [{"name": "value", "email": "value"},...]
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Maximum length of key is 128 bytes, value 10240 bytes, up to 256 key-value pairs, of total size at most 10240.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        name: str = None,
        description: str = None,
        data_set_id: int = None,
        last_success: int = None,
        last_failure: int = None,
        last_seen: int = None,
        schedule: str = None,
        owner: Dict[str, Any] = None,
        authors: List[Dict[str, Any]] = None,
        metadata: Dict[str, str] = None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.description = description
        self.data_set_id = data_set_id
        self.schedule = schedule
        self.owner = owner
        self.authors = authors
        self.metadata = metadata
        self.last_success = last_success
        self.last_failure = last_failure
        self.last_seen = last_seen
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(Integration, cls)._load(resource, cognite_client)
        return instance

    def __hash__(self):
        return hash(self.external_id)


class IntegrationUpdate(CogniteUpdate):
    """Changes applied to integration

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveIntegrationUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "IntegrationUpdate":
            return self._set(value)

    @property
    def external_id(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "externalId")

    @property
    def name(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "name")

    @property
    def description(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "description")

    @property
    def data_set_id(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "dataSetId")

    @property
    def metadata(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "metadata")

    @property
    def schedule(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "schedule")

    @property
    def owner(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "owner")

    @property
    def authors(self):
        return IntegrationUpdate._PrimitiveIntegrationUpdate(self, "authors")


class IntegrationList(CogniteResourceList):
    _RESOURCE = Integration
    _UPDATE = IntegrationUpdate
