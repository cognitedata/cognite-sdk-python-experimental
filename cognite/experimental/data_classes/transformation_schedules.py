from cognite.client.data_classes._base import *


class TransformationSchedule(CogniteResource):
    """The transformation schedules resource allows running recurrent transformations.

    Args:
        request_scheduler_id: Id of the schedule in request scheduler service.
        id (int): Transformation id.
        external_id (str): Transformation externalId.
        created_at (int): Time when the schedule was created.
        interval (str): Cron expression describes when the function should be called. Use http://www.cronmaker.com to create a cron expression.
        is_paused (bool): If true, the transformation is not scheduled.
        config_id (int): Transformation id for backward compatibility.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        request_scheduler_id: int = None,
        id: int = None,
        external_id: str = None,
        created_at: int = None,
        interval: str = None,
        is_paused: bool = None,
        cognite_client=None,
    ):
        self.request_scheduler_id = request_scheduler_id
        self.id = id
        self.external_id = external_id
        self.created_at = created_at
        self.interval = interval
        self.is_paused = is_paused
        self.cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(TransformationSchedule, cls)._load(resource, cognite_client)
        return instance

    def __hash__(self):
        return hash(self.request_scheduler_id)


class TransformationScheduleList(CogniteResourceList):
    _RESOURCE = TransformationSchedule
    _ASSERT_CLASSES = False
