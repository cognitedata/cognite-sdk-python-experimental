import json as _json
from typing import List, Optional, Union

from cognite.client import CogniteClient, utils
from cognite.client._api_client import APIClient
from requests import Response

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    OidcCredentials,
    Transformation,
    TransformationDestination,
    TransformationJobBlockade,
    TransformationList,
    TransformationSchedule,
    TransformationScheduleList,
    TransformationScheduleUpdate,
)
from cognite.experimental.data_classes.transformations import TransformationFilter


class TransformationSchedulesAPI(APIClient):
    _RESOURCE_PATH = "/transformations/schedules"
    _LIST_CLASS = TransformationScheduleList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self, schedule: Union[TransformationSchedule, List[TransformationSchedule]]
    ) -> Union[TransformationSchedule, TransformationScheduleList]:
        """`Schedule the specified transformation with the specified configuration(s). <https://docs.cognite.com/api/playground/#operation/scheduleTransformations>`_

        Args:
            schedule (Union[TransformationSchedule, List[TransformationSchedule]]): Configuration or list of configurations of the schedules to create.

        Returns:
            Created schedule(s)

        Examples:

            Create new schedules:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import TransformationSchedule
                >>> c = CogniteClient()
                >>> schedules = [TransformationSchedule(id = 1, interval = "0 * * * *"), TransformationSchedule(external_id="transformation2", interval = "5 * * * *"))]
                >>> res = c.transformations.schedules.create(schedules)
        """
        utils._auxiliary.assert_type(schedule, "schedule", [TransformationSchedule, list])
        return self._create_multiple(schedule)

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[TransformationSchedule]:
        """`Retrieve a single transformation schedule by the id or external id of its transformation. <https://docs.cognite.com/api/playground/#operation/getTransformationSchedule>`_

        Args:
            id (int, optional): transformation ID
            external_id (str, optional): transformation External ID

        Returns:
            Optional[TransformationSchedule]: Requested transformation schedule or None if it does not exist.

        Examples:

            Get transformation schedule by transformation id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.transformations.schedules.retrieve(id=1)

            Get transformation schedule by transformation external id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.transformations.schedules.retrieve(external_id="1")
        """
        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def list(self, include_public: bool = True, limit: Optional[int] = LIST_LIMIT_DEFAULT,) -> TransformationList:
        """`List all transformation schedules. <https://docs.cognite.com/api/playground/#operation/transformationSchedules>`_

        Args:
            include_public (bool): Whether public transformations should be included in the results. (default true).
            cursor (str): Cursor for paging through results.
            limit (int): Limits the number of results to be returned. To retrieve all results use limit=-1, default limit is 25.

        Returns:
            TransformationList: List of transformations

        Example:

            List transformations::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> transformations_list = c.transformations.list()
        """
        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        filter = TransformationFilter(include_public=include_public).dump(camel_case=True)

        return self._list(method="GET", limit=limit, filter=filter,)

    def delete(
        self,
        id: Union[int, List[int]] = None,
        external_id: Union[str, List[str]] = None,
        ignore_unknown_ids: bool = False,
    ) -> None:
        """`Unschedule one or more transformations <https://doc.cognitedata.com/api/playground/#operation/deleteSchedules>`_

        Args:
            id (Union[int, List[int]): Id or list of ids
            external_id (Union[str, List[str]]): External ID or list of exgernal ids
            ignore_unknown_ids (bool): Ignore IDs and external IDs that are not found rather than throw an exception.

        Returns:
            None

        Examples:

            Delete schedules by id or external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.transformations.schedules.delete(id=[1,2,3], external_id="3")
        """
        self._delete_multiple(
            ids=id, external_ids=external_id, wrap_ids=True, extra_body_fields={"ignoreUnknownIds": ignore_unknown_ids},
        )

    def update(
        self,
        item: Union[
            TransformationSchedule,
            TransformationScheduleUpdate,
            List[Union[TransformationSchedule, TransformationScheduleUpdate]],
        ],
    ) -> Union[TransformationSchedule, TransformationScheduleList]:
        """`Update one or more transformation schedules <https://docs.cognite.com/api/playground/#operation/updateTransformationSchedules>`_

        Args:
            item (Union[TransformationSchedule, TransformationScheduleUpdate, List[Union[TransformationSchedule, TransformationScheduleUpdate]]]): Transformation schedule(s) to update

        Returns:
            Union[TransformationSchedule, TransformationScheduleList]: Updated transformation schedule(s)

        Examples:

            Update a transformation schedule that you have fetched. This will perform a full update of the schedule::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> transformation_schedule = c.transformations.schedules.retrieve(id=1)
                >>> transformation_schedule.is_paused = True
                >>> res = c.transformations.update(transformation)

            Perform a partial update on a transformation schedule, updating the interval and unpausing it::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import TransformationScheduleUpdate
                >>> c = CogniteClient()
                >>> my_update = TransformationScheduleUpdate(id=1).interval.set("0 * * * *").is_paused.set(False)
                >>> res = c.transformations.schedules.update(my_update)
        """
        return self._update_multiple(items=item)