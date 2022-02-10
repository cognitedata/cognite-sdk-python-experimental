import uuid

import pytest
from cognite.client.data_classes.geospatial import Feature, FeatureType

from cognite.experimental import CogniteClient

COGNITE_CLIENT = CogniteClient(max_workers=1)


@pytest.fixture(params=[None, "sdk_test"])
def cognite_domain(request):
    yield request.param


@pytest.fixture()
def test_feature_type(cognite_domain):
    COGNITE_CLIENT.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = COGNITE_CLIENT.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id,
            properties={
                "position": {"type": "POINT", "srid": "4326", "optional": "true"},
                "volume": {"type": "DOUBLE"},
                "temperature": {"type": "DOUBLE"},
                "pressure": {"type": "DOUBLE"},
            },
            search_spec={"vol_press_idx": {"properties": ["volume", "pressure"]}},
        )
    )
    yield feature_type
    COGNITE_CLIENT.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture
def test_feature(test_feature_type):
    external_id = f"F_{uuid.uuid4().hex[:10]}"
    feature = COGNITE_CLIENT.geospatial.create_features(
        test_feature_type.external_id,
        Feature(
            external_id=external_id,
            position={"wkt": "POINT(2.2768485 48.8589506)"},
            temperature=12.4,
            volume=1212.0,
            pressure=2121.0,
        ),
    )
    yield feature
    COGNITE_CLIENT.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)


class TestGeospatialAPI:

    # This test already exist in the main python sdk
    # It is repeated here to test the geospatial domain part.
    def test_create_features(self, test_feature_type):
        external_id = f"F_{uuid.uuid4().hex[:10]}"
        COGNITE_CLIENT.geospatial.create_features(
            test_feature_type.external_id,
            Feature(
                external_id=external_id,
                position={"wkt": "POINT(50 50)"},
                temperature=12.4,
                volume=1212.0,
                pressure=2121.0,
            ),
        )
        COGNITE_CLIENT.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)
