import uuid

import pytest
from cognite.client.data_classes.geospatial import Feature, FeatureType

from cognite.experimental import CogniteClient


@pytest.fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient()


@pytest.fixture(params=[None, "sdk_test"])
def cognite_domain(request):
    yield request.param


@pytest.fixture()
def test_feature_type(cognite_client, cognite_domain):
    cognite_client.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = cognite_client.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id,
            properties={
                "position": {"type": "POINT", "srid": "4326", "optional": "true"},
                "volume": {"type": "DOUBLE"},
                "temperature": {"type": "DOUBLE"},
                "pressure": {"type": "DOUBLE"},
                "raster": {"srid": 3857, "type": "RASTER", "storage": "embedded", "optional": True},
            },
            search_spec={"vol_press_idx": {"properties": ["volume", "pressure"]}},
        )
    )
    yield feature_type
    cognite_client.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture
def test_feature(cognite_client, test_feature_type):
    external_id = f"F_{uuid.uuid4().hex[:10]}"
    feature = cognite_client.geospatial.create_features(
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
    cognite_client.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)


@pytest.fixture
def test_feature(cognite_client, test_feature_type):
    external_id = f"F_{uuid.uuid4().hex[:10]}"
    feature = cognite_client.geospatial.create_features(
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
    cognite_client.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)


# NB: raster tests are for now marked as skip since GCP has GDAL drivers entirely disable.
# There is no way to enable them yet, so testing can be done manually against azure-dev or bluefield
# by commenting out the @pytest.mark.skip annotation
class TestGeospatialAPI:

    # This test already exist in the main python sdk
    # It is repeated here to test the geospatial domain part.
    def test_create_features(self, cognite_client, test_feature_type):
        external_id = f"F_{uuid.uuid4().hex[:10]}"
        cognite_client.geospatial.create_features(
            test_feature_type.external_id,
            Feature(
                external_id=external_id,
                position={"wkt": "POINT(50 50)"},
                temperature=12.4,
                volume=1212.0,
                pressure=2121.0,
            ),
        )
        cognite_client.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)

    @pytest.mark.skip(reason="only runs on azure flexible postgres servers")
    def test_put_raster(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.put_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature.external_id,
            raster_id="raster",
            raster_format="XYZ",
            raster_srid=3857,
            file="tests/tests_integration/test_api/geospatial_data/raster-grid-example.xyz",
        )
        assert res.width == 4
        assert res.height == 5
        assert res.numbands == 1
        assert res.scalex == 1.0
        assert res.scaley == 1.0
        assert res.skewx == 0.0
        assert res.skewy == 0.0
        assert res.srid == 3857
        assert res.upperleftx == -0.5
        assert res.upperlefty == -0.5
