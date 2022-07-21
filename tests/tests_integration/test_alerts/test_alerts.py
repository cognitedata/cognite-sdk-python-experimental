import random
from datetime import datetime, timezone
from time import time
from typing import Callable

from pytest import fixture

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.alerts import Alert, AlertChannel


@fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient(headers={"cdf-version": "alpha"})


@fixture(scope="class")
def base_alert() -> Callable[..., Alert]:
    def create() -> Alert:
        return Alert(
            external_id="test_" + str(time()) + str(random.random()),
            channel_id=1,
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


class TestAlertChannelsIntegration:
    def test_create_1(self, cognite_client, disable_gzip, base_channel, base_alert):
        res = cognite_client.alert_channels.create(base_channel())
        assert "test_" in res.external_id

    def test_create_2(self, cognite_client, disable_gzip, base_channel):
        res = cognite_client.alert_channels.create([base_channel(), base_channel()])

        assert len(res) == 2

    def test_list(self, cognite_client, disable_gzip):
        res = cognite_client.alert_channels.list()

        assert len(res) > 0


class TestAlertsIntegration:
    def test_create_1(self, cognite_client, disable_gzip, base_alert):
        res = cognite_client.alerts.create(base_alert())

        assert res.channel_id == 1

    def test_create_2(self, cognite_client, disable_gzip, base_alert):
        res = cognite_client.alerts.create([base_alert(), base_alert()])

        assert len(res) == 2

    def test_list(self, cognite_client, disable_gzip):
        res = cognite_client.alerts.list(channel_ids=[1])

        assert len(res) > 0
