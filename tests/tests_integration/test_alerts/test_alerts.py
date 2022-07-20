from cognite.experimental import CogniteClient

import pytest

@pytest.fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient(api_subversion="alpha")

class TestAlertChannelsIntegration:
    def test_list(self, cognite_client, disable_gzip):
        res = cognite_client.alert_channels.list()

        assert len(res) > 0
        # assert 1 == cognite_client.alert_channels._post.call_count

class TestAlertsIntegration:
    def test_list(self, cognite_client, disable_gzip):
        res = cognite_client.alerts.list()

        assert len(res) > 0
#         assert 1 == cognite_client.alerts._post.call_count
