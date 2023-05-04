import os
import random
from datetime import datetime, timezone
from typing import Callable, Union

from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from pytest import fixture, mark

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.alerts import (
    Alert,
    AlertChannel,
    AlertChannelUpdate,
    AlertList,
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
    creds = OAuthClientCredentials(
        token_url=os.environ["COGNITE_TOKEN_URL"],
        client_id=os.environ["COGNITE_CLIENT_ID"],
        client_secret=os.environ["COGNITE_CLIENT_SECRET"],
        scopes=[os.environ["COGNITE_TOKEN_SCOPES"]],
    )
    return CogniteClient(
        config=ClientConfig(
            base_url=os.environ["COGNITE_BASE_URL"]
            if os.environ["COGNITE_BASE_URL"]
            else "https://azure-dev.cognitedata.com",
            client_name="experimental",
            project="air-azure-dev",
            headers={"cdf-version": "alpha"},
            credentials=creds,
        )
    )


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
def base_alert_with_triggered_points() -> Callable[..., Alert]:
    def create(channel_external_id: int) -> Alert:
        return Alert(
            # external_id="test_" + CURRENT_TS_STR + str(random.random()),
            channel_external_id=channel_external_id,
            source="inttest",
            level="INFO",
            metadata={"test": "test"},
            value="10 percent",
            triggered_points=[
                {"triggered": True, "timestamp": 1000000},
                {"triggered": True, "timestamp": 1120000},
                {"triggered": True, "timestamp": 3500000},
                {"triggered": False, "timestamp": 4900000},
                {"triggered": True, "timestamp": 5000000},
            ],
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
def base_channel_with_deduplication_rules() -> Callable[..., AlertChannel]:
    def create() -> AlertChannel:
        return AlertChannel(
            external_id="test_" + CURRENT_TS_STR + "_" + str(random.random()),
            name="test_channel_" + CURRENT_TS_STR,
            description="integration test channel with deduplication rules",
            metadata={"test": "test"},
            alert_rules={"deduplication": {"merge_interval": "2m", "activation_interval": "5m"}},
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

    def test_create_3(self, cognite_client, base_channel, base_channel_with_deduplication_rules):
        res = cognite_client.alerts.channels.create([base_channel(), base_channel_with_deduplication_rules()])
        assert len(res) == 2

    def test_list(self, cognite_client):
        res = cognite_client.alerts.channels.list()
        assert len(res) > 0

    def test_update_by_alert_channel(self, cognite_client, base_channel):
        created = cognite_client.alerts.channels.create([base_channel()])[0]

        created.description = "updated description"
        created.external_id = f"{created.external_id}_updated_ext_id"
        created.metadata = {"a": "b"}

        update_res = cognite_client.alerts.channels.update([created])

        updated = cognite_client.alerts.channels.list(ids=[created.id])

        assert update_res == updated

        assert len(updated) == 1
        assert updated[0].description == "updated description"
        assert updated[0].metadata == {"a": "b"}
        assert "updated_ext_id" in updated[0].external_id

    def test_update_by_alert_channel_update(self, cognite_client, base_channel):
        created = cognite_client.alerts.channels.create([base_channel()])[0]

        update = (
            AlertChannelUpdate(created.id)
            .description.set("updated description")
            .external_id.set(f"{created.external_id}_updated_ext_id")
            .metadata.add({"a": "b"})
        )

        update_res = cognite_client.alerts.channels.update([update])

        updated = cognite_client.alerts.channels.list(ids=[created.id])

        assert update_res == updated

        assert len(updated) == 1
        assert updated[0].description == "updated description"
        assert updated[0].metadata == {"a": "b", "test": "test"}
        assert "updated_ext_id" in updated[0].external_id

    def test_delete_channel(self, cognite_client, base_channel):
        created = cognite_client.alerts.channels.create(base_channel())

        cognite_client.alerts.channels.delete(external_ids=[created.external_id])

        res = cognite_client.alerts.channels.list(external_ids=[created.external_id])

        assert len(res) == 0

    def test_delete_channel_with_deduplication_rules(self, cognite_client, base_channel_with_deduplication_rules):
        created = cognite_client.alerts.channels.create(base_channel_with_deduplication_rules())

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

    def test_create_3(self, cognite_client, base_alert_with_triggered_points, base_channel_with_deduplication_rules):
        channel = cognite_client.alerts.channels.create(base_channel_with_deduplication_rules())

        res = cognite_client.alerts.create_deduplicated(base_alert_with_triggered_points(channel.external_id))
        assert isinstance(res, Union[Alert, AlertList])
        assert channel.external_id == res.channel_external_id

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
