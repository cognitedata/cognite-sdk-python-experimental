from cognite.client.data_classes._base import *


class IntegrationWithStatuses(CogniteResource):
    """A representation of a response with list of Runs.

    Args:
        external_id (str): The external ID of related integration provided by the client. Must be unique for the resource type.
        statuses (List[Dict[str, Any]]): List of Runs represented as statuses.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self, external_id: str = None, statuses: List[Dict[str, Any]] = None, cognite_client=None,
    ):
        setattr(self, "external_id", external_id),
        self.statuses = (statuses,)
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(IntegrationWithStatuses, cls)._load(resource, cognite_client)
        return instance

    def runs(self):
        result: List[IntegrationRun] = []
        if len(self.statuses) > 0:
            for status in self.statuses:
                if not (status is None):
                    result.append(
                        IntegrationRun(self.external_id, status["status"], status.get("message"), status["createdTime"])
                    )
        return result


class IntegrationRun(CogniteResource):
    """A representation of a IntegrationRun.

    Args:
        external_id (str): The external ID of related integration provided by the client. Must be unique for the resource type.
        status (str): success/failure/seen.
        message (str): failure message.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        external_id: str = None,
        status: str = None,
        message: str = None,
        created_time: int = None,
        cognite_client=None,
    ):
        setattr(self, "external_id", external_id)
        setattr(self, "status", status)
        setattr(self, "message", message)
        setattr(self, "created_time", created_time)
        self._cognite_client = cognite_client


class IntegrationWithStatusesUpdate(CogniteUpdate):
    class _PrimitiveIntegrationWithStatusesUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "IntegrationWithStatusesUpdate":
            return self._set(value)


class IntegrationRunUpdate(CogniteUpdate):
    class _PrimitiveIntegrationRunUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "IntegrationRunUpdate":
            return self._set(value)


class IntegrationWithStatusesList(CogniteResourceList):
    _RESOURCE = IntegrationWithStatuses
    _UPDATE = IntegrationWithStatusesUpdate


class IntegrationRunList(CogniteResourceList):
    _RESOURCE = IntegrationRun
    _UPDATE = IntegrationRunUpdate
