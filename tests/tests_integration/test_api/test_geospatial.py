import os

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.geospatial import FeatureType

COGNITE_CLIENT = CogniteClient()
COGNITE_DISABLE_GZIP = "COGNITE_DISABLE_GZIP"


@pytest.fixture
def new_feature_type():
    feature_type = COGNITE_CLIENT.geospatial.create_feature_types(
        FeatureType(external_id="my_feature_type", attributes={"temperature": {"type": "DOUBLE"}})
    )
    yield feature_type
    COGNITE_CLIENT.geospatial.delete_feature_types(external_id="my_feature_type")


@pytest.fixture(autouse=True)
def disable_gzip():
    v = os.getenv(COGNITE_DISABLE_GZIP)
    os.environ[COGNITE_DISABLE_GZIP] = "true"
    yield
    if v is None:
        os.environ.pop(COGNITE_DISABLE_GZIP)
    else:
        os.environ[COGNITE_DISABLE_GZIP] = v


class TestGeospatialAPI:
    @pytest.mark.skip(reason="Failing sporadically. Vincent will follow up with PR to make it more robust.")
    def test_retrieve_external_id(self, new_feature_type):
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        assert res[0] == COGNITE_CLIENT.geospatial.retrieve_feature_types(external_id=res[0].external_id)

    def test_list(self, new_feature_type):
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        assert 0 < len(res) < 100
