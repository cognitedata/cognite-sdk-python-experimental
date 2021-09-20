from cognite.client.data_classes._base import *


class ExtractionPipeline(CogniteResource):
    """A representation of an ExtractionPipeline.

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
        name (str): The name of the ExtractionPipeline.
        description (str): The description of the ExtractionPipeline.
        data_set_id (int): The id of the dataset this ExtractionPipeline related with.
        raw_tables (List[Dict[str, str]): list of raw tables in list format: [{"dbName": "value", "tableName" : "value"}].
        last_success (int): Milliseconds value of last success status.
        last_failure (int): Milliseconds value of last failure status.
        last_message (str): Message of last failure.
        last_seen (int): Milliseconds value of last seen status.
        schedule (str): undefined/triggered/streamed/cron regex.
        contacts (List[Dict[str, Any]]): list of contacts [{"name": "value", "email": "value", "role": "value", "sendNotification": boolean},...]
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Maximum length of key is 128 bytes, value 10240 bytes, up to 256 key-value pairs, of total size at most 10240.
        source (str): Source text value for ExtractionPipeline.
        documentation (str): Documentation text value for ExtractionPipeline.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        created_by (str): ExtractionPipeline creator, usually email.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        name: str = None,
        description: str = None,
        data_set_id: int = None,
        raw_tables: List[Dict[str, Any]] = None,
        last_success: int = None,
        last_failure: int = None,
        last_message: str = None,
        last_seen: int = None,
        schedule: str = None,
        contacts: List[Dict[str, Any]] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        documentation: str = None,
        created_time: int = None,
        last_updated_time: int = None,
        created_by: str = None,
        cognite_client=None,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.description = description
        self.data_set_id = data_set_id
        self.raw_tables = raw_tables
        self.schedule = schedule
        self.contacts = contacts
        self.metadata = metadata
        self.source = source
        self.documentation = documentation
        self.last_success = last_success
        self.last_failure = last_failure
        self.last_message = last_message
        self.last_seen = last_seen
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by = created_by
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(ExtractionPipeline, cls)._load(resource, cognite_client)
        return instance

    def __hash__(self):
        return hash(self.external_id)


class ExtractionPipelineUpdate(CogniteUpdate):
    """Changes applied to ExtractionPipeline

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveExtractionPipelineUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "ExtractionPipelineUpdate":
            return self._set(value)

    class _ObjectExtractionPipelineUpdate(CogniteObjectUpdate):
        def set(self, value: Dict) -> "ExtractionPipelineUpdate":
            return self._set(value)

        def add(self, value: Dict) -> "ExtractionPipelineUpdate":
            return self._add(value)

        def remove(self, value: List) -> "ExtractionPipelineUpdate":
            return self._remove(value)

    class _ListExtractionPipelineUpdate(CogniteListUpdate):
        def set(self, value: List) -> "ExtractionPipelineUpdate":
            return self._set(value)

        def add(self, value: List) -> "ExtractionPipelineUpdate":
            return self._add(value)

        def remove(self, value: List) -> "ExtractionPipelineUpdate":
            return self._remove(value)

    @property
    def external_id(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "externalId")

    @property
    def name(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "name")

    @property
    def description(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "description")

    @property
    def data_set_id(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "dataSetId")

    @property
    def raw_tables(self):
        return ExtractionPipelineUpdate._ListExtractionPipelineUpdate(self, "rawTables")

    @property
    def metadata(self):
        return ExtractionPipelineUpdate._ObjectExtractionPipelineUpdate(self, "metadata")

    @property
    def source(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "source")

    @property
    def documentation(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "documentation")

    @property
    def schedule(self):
        return ExtractionPipelineUpdate._PrimitiveExtractionPipelineUpdate(self, "schedule")

    @property
    def contacts(self):
        return ExtractionPipelineUpdate._ListExtractionPipelineUpdate(self, "contacts")


class ExtractionPipelineList(CogniteResourceList):
    _RESOURCE = ExtractionPipeline
    _UPDATE = ExtractionPipelineUpdate
