from typing import Dict, List

from cognite.client.utils._auxiliary import to_camel_case

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes.alerts import (
    Alert,
    AlertChannel,
    AlertChannelFilter,
    AlertChannelList,
    AlertFilter,
    AlertList,
)


class AlertsChannelsAPI(ContextAPI):
    _RESOURCE_PATH = "/alerts/channels"
    _LIST_CLASS = AlertChannelList

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

        models = self._post(
            self._RESOURCE_PATH + "/list", json={"filter": filter, "page": 1}, headers={"cdf-version": "alpha"}
        ).json()["items"]

        return AlertChannelList([AlertChannel._load(model, cognite_client=self._cognite_client) for model in models])


class AlertsAPI(ContextAPI):
    _RESOURCE_PATH = "/alerts/alerts"
    _LIST_CLASS = AlertList

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

        models = self._post(
            self._RESOURCE_PATH + "/list", json={"filter": filter, "page": 1}, headers={"cdf-version": "alpha"}
        ).json()["items"]

        return AlertList([Alert._load(model, cognite_client=self._cognite_client) for model in models])
