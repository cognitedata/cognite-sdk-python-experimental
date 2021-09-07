from typing import List, Optional, Union

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    OidcCredentials,
    Transformation,
    TransformationDestination,
    TransformationJobBlockade,
    TransformationList,
    TransformationNotification,
    TransformationNotificationFilter,
    TransformationNotificationList,
)


class TransformationNotificationsAPI(APIClient):
    _RESOURCE_PATH = "/transformations/notifications"
    _LIST_CLASS = TransformationNotificationList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self, notification: Union[TransformationNotification, List[TransformationNotification]]
    ) -> Union[TransformationNotification, TransformationNotificationList]:
        """`Subscribe for notifications on the transformation errors. <https://docs.cognite.com/api/playground/#operation/subscribeTransformationNotifications>`_

        Args:
            notification (Union[TransformationNotification, List[TransformationNotification]]): Notification or list of notifications to create.

        Returns:
            Created notification(s)

        Examples:

            Create new notifications:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import TransformationNotification
                >>> c = CogniteClient()
                >>> notifications = [TransformationNotification(transformation_id = 1, destination="my@email.com"), TransformationNotification(transformation_external_id="transformation2", destination="other@email.com"))]
                >>> res = c.transformations.notifications.create(notifications)
        """
        utils._auxiliary.assert_type(notification, "notification", [TransformationNotification, list])
        return self._create_multiple(notification)

    def list(
        self,
        transformation_id: Optional[int] = None,
        transformation_external_id: str = None,
        limit: Optional[int] = LIST_LIMIT_DEFAULT,
    ) -> TransformationNotificationList:
        """`List notification subscriptions. <https://docs.cognite.com/api/playground/#operation/listTransformationNotifications>`_

        Args:
            transformation_id (Optional[int]): List only notifications for the specified transformation. The transformation is identified by internal numeric ID.
            transformation_external_id (str): List only notifications for the specified transformation. The transformation is identified by externalId.
            limit (int): Limits the number of results to be returned. To retrieve all results use limit=-1, default limit is 25.

        Returns:
            TransformationNotificationList: List of transformation notifications

        Example:

            List all notifications::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> notifications_list = c.transformations.notifications.list()
            
            List all notifications by transformation id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> notifications_list = c.transformations.notifications.list(transformation_id = 1)

            List all notifications by transformation external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> notifications_list = c.transformations.notifications.list(transformation_external_id = "myExternalId")
        """
        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        filter = TransformationNotificationFilter(
            transformation_id=transformation_id, transformation_external_id=transformation_external_id
        ).dump(camel_case=True)

        return self._list(method="GET", limit=limit, filter=filter,)

    def delete(self, id: Union[int, List[int]] = None,) -> None:
        """`Deletes the specified notification subscriptions on the transformation. Does nothing when the subscriptions already don't exist <https://doc.cognitedata.com/api/playground/#operation/deleteTransformationNotifications>`_

        Args:
            id (Union[int, List[int]): Id or list of ids

        Returns:
            None

        Examples:

            Delete schedules by id or external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.transformations.notifications.delete(id=[1,2,3])
        """
        self._delete_multiple(
            ids=id, wrap_ids=True,
        )
