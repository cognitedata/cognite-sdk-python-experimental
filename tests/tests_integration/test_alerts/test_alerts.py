import random
from datetime import datetime, timezone
from time import time
from typing import Callable

from pytest import fixture

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.alerts import (
    Alert,
    AlertChannel,
    AlertSubscriber,
    AlertSubscription,
    AlertSubscriptionDelete,
)

ALERTS_INT_TEST_EMAIL = f"ivan.polomanyi+{str(time())}@cognite.com"


@fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient(headers={"cdf-version": "alpha"})


@fixture(scope="class")
def base_alert() -> Callable[..., Alert]:
    def create(channel_external_id: int) -> Alert:
        return Alert(
            external_id="test_" + str(time()) + str(random.random()),
            channel_external_id=channel_external_id,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            source="inttest",
            level="INFO",
            metadata={"test": "test"},
            value="10 percent",
        )

    return create


@fixture(scope="class")
def base_channel() -> Callable[..., AlertChannel]:
    def create() -> AlertChannel:
        return AlertChannel(
            external_id="test_" + str(time()) + "_" + str(random.random()),
            name="test_channel_" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            description="integration test channel",
            metadata={"test": "test"},
        )

    return create


@fixture(scope="class")
def base_subscriber() -> Callable[..., AlertSubscriber]:
    def create() -> AlertSubscriber:
        return AlertSubscriber(
            external_id="test_" + str(time()) + str(random.random()),
            metadata={"test": "test"},
            email=ALERTS_INT_TEST_EMAIL,
        )

    return create


@fixture(scope="class")
def base_subscription() -> Callable[..., AlertSubscription]:
    def create(subscriber_id: int) -> AlertSubscription:
        return AlertSubscription(
            external_id="test_" + str(time()) + str(random.random()),
            channel_id=1,
            subscriber_id=subscriber_id,
            metadata={"test": "test"},
        )

    return create


class TestAlertChannelsIntegration:
    def test_create_1(self, cognite_client, base_channel):
        res = cognite_client.alerts.channels.create(base_channel())
        assert "test_" in res.external_id

    def test_create_2(self, cognite_client, base_channel):
        res = cognite_client.alerts.channels.create([base_channel(), base_channel()])

        assert len(res) == 2

    def test_list(self, cognite_client, disable_gzip):
        res = cognite_client.alerts.channels.list()

        assert len(res) > 0


class TestAlertsIntegration:
    def test_create_1(self, cognite_client, base_alert, base_channel):
        channel = cognite_client.alerts.channels.create(base_channel())

        res = cognite_client.alerts.create(base_alert(channel.external_id))

        assert channel.external_id == res.channel_external_id

    def test_create_2(self, cognite_client, base_alert, base_channel):
        channel = cognite_client.alerts.channels.create(base_channel())

        res = cognite_client.alerts.create([base_alert(channel.external_id), base_alert(channel.external_id)])

        assert len(res) == 2

    def test_list(self, cognite_client):
        res = cognite_client.alerts.list()

        assert len(res) > 0


class TestSubscribersIntegration:
    def test_create_1(self, cognite_client, base_subscriber):
        res = cognite_client.alerts.subscribers.create(base_subscriber())

        assert ALERTS_INT_TEST_EMAIL == res.email


class TestSubscriptionsIntegration:
    def test_create_1(self, cognite_client, base_subscription, base_subscriber):
        subscriber = cognite_client.alerts.subscribers.create(base_subscriber())

        res = cognite_client.alerts.subscriptions.create(base_subscription(subscriber.id))

        assert res.channel_id == 1

    def test_delete_by_subscriber_and_channel(self, cognite_client, base_subscription, base_subscriber):
        subscriber = cognite_client.alerts.subscribers.create(base_subscriber())

        item = cognite_client.alerts.subscriptions.create(base_subscription(subscriber.id))

        delete_item = AlertSubscriptionDelete(channel_id=item.channel_id, subscriber_id=item.subscriber_id)
        res = cognite_client.alerts.subscriptions.delete([delete_item])

        assert res == None
