from datetime import datetime
from unittest import mock

import pytest

import cognite.client.utils._time
from cognite.client.utils._auxiliary import random_string
from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Asset, AssetUpdate, Label, LabelFilter, LabelList
from tests.utils import set_request_limit

COGNITE_CLIENT = CogniteClient()


@pytest.fixture
def new_label():
    tp = COGNITE_CLIENT.labels.create(Label(external_id=random_string(30)))
    yield tp
    COGNITE_CLIENT.labels.delete(external_id=tp.external_id)


@pytest.fixture
def post_spy():
    with mock.patch.object(COGNITE_CLIENT.labels, "_post", wraps=COGNITE_CLIENT.labels._post) as _:
        yield


class TestLabelsAPI:
    def test_list(self, post_spy):
        res = COGNITE_CLIENT.labels.list()
        assert 0 < len(res) < 100
        assert 1 == COGNITE_CLIENT.labels._post.call_count

    def test_create_asset_with_label(self, new_label):
        labels = [{"externalId": new_label.external_id}]
        ac = COGNITE_CLIENT.assets_playground.create(Asset(name="any", labels=labels))
        assert isinstance(ac, Asset)
        assert labels == ac.labels
        COGNITE_CLIENT.assets_playground.delete(id=ac.id)

    def test_update_asset_with_label(self, new_label):
        ac = COGNITE_CLIENT.assets_playground.create(Asset(name="any", description="delete me"))
        assert not ac.labels
        update = AssetUpdate(id=ac.id)
        update = update.put_label(external_id=new_label.external_id)
        assert isinstance(update, AssetUpdate)
        ua = COGNITE_CLIENT.assets_playground.update(update)
        assert len(ua.labels) == 1
        assert new_label.external_id == ua.labels[0]["externalId"]

        update = AssetUpdate(id=ac.id)
        update = update.remove_label(external_id=new_label.external_id)
        assert isinstance(update, AssetUpdate)
        ua = COGNITE_CLIENT.assets_playground.update(update)

        assert not ua.labels
        COGNITE_CLIENT.assets_playground.delete(id=ac.id)
