from enum import Enum
from uuid import UUID

from cognite.client.data_classes._base import *


class TransformationJobStatus(str, Enum):
    RUNNING = "Running"
    CREATED = "Created"
    COMPLETED = "Completed"
    FAILED = "Failed"


class TransformationJob(CogniteResource):
    """The transformation joob resource allows following the status of execution of a transformation run.

    Args:
        id (int): A server-generated ID for the object.
        uuid (UUID): A server-generated UUID for the object.
        status (TransformationJobStatus): Status of the job.
        source_project (str): Name of the cdf project where the data will be read from.
        destination_project (str): Name of the cdf project where the data will be written to.
        destination_type (str): Target resource type of the transformation.
        destination_database (str): Target detabase if the destination type is raw.
        destination_table (str): Target table name if the destination type is raw.
        conflict_mode (str): What to do in case of id collisions: either "abort", "upsert", "update" or "delete".
        raw_query (str): Query of the transformation that is being executed.
        error (str): Error message from the server.
        ignore_null_fields (bool): Indicates how null values are handled on updates: ignore or set null.
        created_time (int): Time when the job was created.
        started_time (int): Time when the job started running.
        finished_time (int): Time when the job finished running.
        last_seen_time (int): Time of the last status update from the job.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        id: int = None,
        uuid: UUID = None,
        status: TransformationJobStatus = None,
        source_project: str = None,
        destination_project: str = None,
        destination_type: str = None,
        destination_database: str = None,
        destination_table: str = None,
        conflict_mode: str = None,
        raw_query: str = None,
        error: str = None,
        ignore_null_fields: bool = False,
        created_time: int = None,
        started_time: int = None,
        finished_time: int = None,
        last_seen_time: int = None,
        cognite_client=None,
    ):
        self.id = id
        self.uuid = uuid
        self.status = status
        self.source_project = source_project
        self.destination_project = destination_project
        self.destination_type = destination_type
        self.destination_database = destination_database
        self.destination_table = destination_table
        self.conflict_mode = conflict_mode
        self.raw_query = raw_query
        self.error = error
        self.ignore_null_fields = ignore_null_fields
        self.created_time = created_time
        self.started_time = started_time
        self.finished_time = finished_time
        self.last_seen_time = last_seen_time
        self.cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(TransformationJob, cls)._load(resource, cognite_client)
        return instance

    def __hash__(self):
        return hash(self.id)


class TransformationJobList(CogniteResourceList):
    _RESOURCE = TransformationJob
    _ASSERT_CLASSES = False
