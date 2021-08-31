import os

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.geospatial import Feature, FeatureType

COGNITE_CLIENT = CogniteClient()
COGNITE_DISABLE_GZIP = "COGNITE_DISABLE_GZIP"


@pytest.fixture
def new_feature_type():
    feature_type = COGNITE_CLIENT.geospatial.create_feature_types(
        FeatureType(external_id="my_feature_type", attributes={"temperature": {"type": "DOUBLE"}})
    )
    yield feature_type
    COGNITE_CLIENT.geospatial.delete_feature_types(external_id="my_feature_type")


@pytest.fixture
def new_feature(new_feature_type):
    feature = COGNITE_CLIENT.geospatial.create_features(
        new_feature_type, Feature(external_id="my_feature", temperature=12.4)
    )
    yield feature
    COGNITE_CLIENT.geospatial.delete_features(new_feature_type, external_id="my_feature")


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
    def test_retrieve_feature_type_by_external_id(self, new_feature_type):
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        assert res[0] == COGNITE_CLIENT.geospatial.retrieve_feature_types(external_id=res[0].external_id)

    def test_list_feature_types(self, new_feature_type):
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        assert 0 < len(res) < 100

    def test_retrieve_feature_by_external_id(self, new_feature_type, new_feature):
        res = COGNITE_CLIENT.geospatial.retrieve_features(
            feature_type=new_feature_type, external_id=new_feature.external_id
        )
        assert res.external_id == new_feature.external_id
