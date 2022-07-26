from typing import Dict, List, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type, to_camel_case

from cognite.experimental.data_classes.alerts import (
    Alert,
    AlertChannel,
    AlertChannelFilter,
    AlertChannelList,
    AlertChannelUpdate,
    AlertFilter,
    AlertList,
    AlertSubscriber,
    AlertSubscriberList,
    AlertSubscription,
    AlertSubscriptionDelete,
    AlertSubscriptionList,
)


class AlertsChannelsAPI(APIClient):
    _RESOURCE_PATH = "/alerts/channels"
    _LIST_CLASS = AlertChannelList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self,
        alert_channels: Union[AlertChannel, List[AlertChannel]],
    ) -> Union[AlertChannel, AlertChannelList]:
        assert_type(alert_channels, "alert_channels", [AlertChannel, list])
        return self._create_multiple(
            items=alert_channels,
            resource_path=self._RESOURCE_PATH,
            list_cls=AlertChannelList,
            resource_cls=AlertChannel,
        )

    def list(
        self,
        external_ids: List[str] = None,
        ids: List[int] = None,
        parent_ids: List[str] = None,
        metadata: Dict[str, str] = None,
        limit=100,
    ) -> AlertChannelList:
        """List alert channels

        Args:
            ids: channel ids.


        Returns:
            AlertChannelList: list of channels"""

        filter = AlertChannelFilter(
            external_ids=external_ids,
            ids=ids,
            parent_ids=parent_ids,
            metadata=metadata,
        ).dump(camel_case=True)
        filter = {to_camel_case(k): v for k, v in (filter or {}).items() if v is not None}

        return self._list(
            method="POST", limit=limit, filter=filter, list_cls=AlertChannelList, resource_cls=AlertChannel
        )

    def update(
        self, items: Union[AlertChannel, AlertChannelUpdate, List[Union[AlertChannel, AlertChannelUpdate]]]
    ) -> Union[AlertChannel, AlertChannelList]:
        """Update alerting channels

        Args:
            items: Union[AlertChannel, AlertChannelUpdate, List[Union[AlertChannel, AlertChannelUpdate]]]: items to be updated
        """
        return self._update_multiple(
            items=items, list_cls=AlertChannelList, resource_cls=AlertChannel, update_cls=AlertChannelUpdate
        )

    def delete(self, ids: List[int] = None, external_ids: List[str] = None) -> None:
        self._delete_multiple(ids=ids, external_ids=external_ids, wrap_ids=True)


class AlertSubscribersAPI(APIClient):
    _RESOURCE_PATH = "/alerts/subscribers"
    _LIST_CLASS = AlertSubscriberList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self,
        alerts_subscribers: Union[AlertSubscriber, List[AlertSubscriber]],
    ) -> Union[AlertSubscriber, AlertSubscriberList]:
        assert_type(alerts_subscribers, "alerts_subscribers", [AlertSubscriber, list])
        return self._create_multiple(
            items=alerts_subscribers,
            resource_path=self._RESOURCE_PATH,
            list_cls=AlertSubscriberList,
            resource_cls=AlertSubscriber,
        )


class AlertSubscriptionsAPI(APIClient):
    _RESOURCE_PATH = "/alerts/subscriptions"
    _LIST_CLASS = AlertSubscriptionList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(
        self,
        alerts_subscriptions: Union[AlertSubscription, List[AlertSubscriptionList]],
    ) -> Union[AlertSubscription, AlertSubscriptionList]:
        assert_type(alerts_subscriptions, "alerts_subscriptions", [AlertSubscription, list])
        return self._create_multiple(
            items=alerts_subscriptions,
            resource_path=self._RESOURCE_PATH,
            list_cls=AlertSubscriptionList,
            resource_cls=AlertSubscription,
        )

    def delete(self, cmds: List[AlertSubscriptionDelete]) -> None:
        items_to_delete = [cmd.dump(camel_case=True) for cmd in cmds]

        body = {"items": items_to_delete}
        url = self._RESOURCE_PATH + "/delete"
        self._post(url, json=body)


class AlertsAPI(APIClient):
    _RESOURCE_PATH = "/alerts/alerts"
    _LIST_CLASS = AlertList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = AlertsChannelsAPI(*args, **kwargs)
        self.subscribers = AlertSubscribersAPI(*args, **kwargs)
        self.subscriptions = AlertSubscriptionsAPI(*args, **kwargs)

    def create(
        self,
        alerts: Union[Alert, List[Alert]],
    ) -> Union[Alert, AlertList]:
        assert_type(alerts, "alerts", [Alert, list])
        return self._create_multiple(
            items=alerts, resource_path=self._RESOURCE_PATH, list_cls=AlertList, resource_cls=Alert
        )

    def list(
        self,
        ids: List[int] = None,
        external_ids: List[str] = None,
        channel_ids: List[int] = None,
        channel_external_ids: List[int] = None,
        closed: bool = None,
        start_time: str = None,
        end_time: str = None,
        limit=100,
    ) -> AlertList:
        """List alerts

        Args:
            ids: alert ids to filter


        Returns:
            AlertsList: list of alerts"""

        filter = AlertFilter(
            ids=ids,
            external_ids=external_ids,
            channel_ids=channel_ids,
            channel_external_ids=channel_external_ids,
            closed=closed,
            start_time=start_time,
            end_time=end_time,
        ).dump(camel_case=True)
        filter = {to_camel_case(k): v for k, v in (filter or {}).items() if v is not None}

        return self._list(method="POST", limit=limit, filter=filter, list_cls=AlertList, resource_cls=Alert)

    def close(
        self,
        ids: List[int] = None,
        external_ids: List[str] = None,
    ) -> None:
        """Close an alert

        Args:
            ids: alert ids to close
            external_ids: alert external_ids to close


        Returns:
            None"""

        all_ids = self._process_ids(ids, external_ids, wrap_ids=True)

        self._post(self._RESOURCE_PATH + "/close", json={"items": all_ids}, headers={"cdf-version": "alpha"}).json()

        return None
