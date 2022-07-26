import os
import random
from datetime import datetime, timezone
from time import time
from typing import Callable

from pytest import fixture, mark

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.alerts import (
    Alert,
    AlertChannel,
    AlertSubscriber,
    AlertSubscription,
    AlertSubscriptionDelete,
)

CURRENT_TS = datetime.now(timezone.utc)
CURRENT_TS_INT = int(CURRENT_TS.timestamp())
CURRENT_TS_STR = CURRENT_TS.strftime("%Y-%m-%dT%H:%M:%S")
ALERTS_INT_TEST_EMAIL = f"ivan.polomanyi+{CURRENT_TS_INT}@cognite.com"


@fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient(headers={"cdf-version": "alpha"})


@fixture(scope="class")
def base_alert() -> Callable[..., Alert]:
    def create(channel_external_id: int) -> Alert:
        return Alert(
            external_id="test_" + CURRENT_TS_STR + str(random.random()),
            channel_external_id=channel_external_id,
            timestamp=CURRENT_TS_INT,
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
            external_id="test_" + CURRENT_TS_STR + "_" + str(random.random()),
            name="test_channel_" + CURRENT_TS_STR,
            description="integration test channel",
            metadata={"test": "test"},
        )

    return create


@fixture(scope="class")
def base_subscriber() -> Callable[..., AlertSubscriber]:
    def create() -> AlertSubscriber:
        return AlertSubscriber(
            external_id="test_" + CURRENT_TS_STR + str(random.random()),
            metadata={"test": "test"},
            email=ALERTS_INT_TEST_EMAIL,
        )

    return create


@fixture(scope="class")
def base_subscription() -> Callable[..., AlertSubscription]:
    def create(channel_id: int, subscriber_id: int) -> AlertSubscription:
        return AlertSubscription(
            external_id="test_" + CURRENT_TS_STR + str(random.random()),
            channel_id=channel_id,
            subscriber_id=subscriber_id,
            metadata={"test": "test"},
        )

    return create


@mark.skipif(
    os.environ.get("ENABLE_ALERTS_TESTS") == None, reason="Skipping alerts API tests due to service immaturity"
)
class TestAlertChannelsIntegration:
    def test_create_1(self, cognite_client, base_channel):
        res = cognite_client.alerts.channels.create(base_channel())
        assert "test_" in res.external_id

    def test_create_2(self, cognite_client, base_channel):
        res = cognite_client.alerts.channels.create([base_channel(), base_channel()])

        assert len(res) == 2

    def test_list(self, cognite_client):
        res = cognite_client.alerts.channels.list()

        assert len(res) > 0

    def test_delete(self, cognite_client, base_channel):
        created = cognite_client.alerts.channels.create(base_channel())

        cognite_client.alerts.channels.delete(external_ids=[created.external_id])

        res = cognite_client.alerts.channels.list(external_ids=[created.external_id])

        assert len(res) == 0


@mark.skipif(
    os.environ.get("ENABLE_ALERTS_TESTS") == None, reason="Skipping alerts API tests due to service immaturity"
)
class TestAlertsIntegration:
    def test_create_1(self, cognite_client, base_alert, base_channel):
        channel = cognite_client.alerts.channels.create(base_channel())

        res = cognite_client.alerts.create(base_alert(channel.external_id))

        assert channel.external_id == res.channel_external_id

    def test_create_2(self, cognite_client, base_alert, base_channel):
        channel = cognite_client.alerts.channels.create(base_channel())

        res = cognite_client.alerts.create([base_alert(channel.external_id), base_alert(channel.external_id)])

        assert len(res) == 2

    def test_close(self, cognite_client):
        alerts = cognite_client.alerts.list(closed=False)

        cognite_client.alerts.close(ids=[alerts[0].id])

        check_closed = cognite_client.alerts.list(ids=[alerts[0].id])

        assert check_closed[0].closed == True
        assert len(check_closed) == 1
        assert check_closed[0].id == alerts[0].id

    def test_list(self, cognite_client):
        res = cognite_client.alerts.list()

        assert len(res) > 0


@mark.skipif(
    os.environ.get("ENABLE_ALERTS_TESTS") == None, reason="Skipping alerts API tests due to service immaturity"
)
class TestSubscribersIntegration:
    def test_create_1(self, cognite_client, base_subscriber):
        res = cognite_client.alerts.subscribers.create(base_subscriber())

        assert ALERTS_INT_TEST_EMAIL == res.email


@mark.skipif(
    os.environ.get("ENABLE_ALERTS_TESTS") == None, reason="Skipping alerts API tests due to service immaturity"
)
class TestSubscriptionsIntegration:
    def test_create_1(self, cognite_client, base_subscription, base_subscriber, base_channel):
        channel = cognite_client.alerts.channels.create(base_channel())

        subscriber = cognite_client.alerts.subscribers.create(base_subscriber())

        res = cognite_client.alerts.subscriptions.create(base_subscription(channel.id, subscriber.id))

        assert res.channel_id == channel.id

    def test_delete_by_subscriber_and_channel(self, cognite_client, base_subscription, base_channel, base_subscriber):
        channel = cognite_client.alerts.channels.create(base_channel())

        subscriber = cognite_client.alerts.subscribers.create(base_subscriber())

        item = cognite_client.alerts.subscriptions.create(base_subscription(channel.id, subscriber.id))

        delete_item = AlertSubscriptionDelete(channel_id=item.channel_id, subscriber_id=item.subscriber_id)
        res = cognite_client.alerts.subscriptions.delete([delete_item])

        assert res == None
