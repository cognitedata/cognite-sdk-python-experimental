import uuid

import pytest
from cognite.client.data_classes.geospatial import *
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.geospatial import FeatureType as ExperimentalFeatureType
from cognite.experimental.data_classes.geospatial import *


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
    external_id = f"F/O@ö_{uuid.uuid4().hex[:10]}"
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
def test_feature_with_raster(cognite_client, test_feature_type, test_feature):
    cognite_client.geospatial.put_raster(
        feature_type_external_id=test_feature_type.external_id,
        feature_external_id=test_feature.external_id,
        raster_property_name="raster",
        raster_format="XYZ",
        raster_srid=3857,
        file="tests/tests_integration/test_api/geospatial_data/raster-grid-example.xyz",
    )
    yield test_feature


@pytest.fixture
def test_mvt_mappings_def(cognite_client, test_feature_type):
    external_id = f"MVT/O@ö_{uuid.uuid4().hex[:10]}"
    mvt_mappings_def = cognite_client.geospatial.create_mvt_mappings_definitions(
        MvpMappingsDefinition(
            external_id=external_id,
            mappings=[
                {
                    "featureTypeExternalId": test_feature_type.external_id,
                    "levels": [0, 1, 2, 3, 4, 5],
                    "geometryProperty": "position",
                    "featureProperties": ["volume", "temperature"],
                }
            ],
        )
    )
    yield mvt_mappings_def
    cognite_client.geospatial.delete_mvt_mappings_definitions(external_id=external_id)


class TestExperimentalGeospatialAPI:
    def test_create_feature_type_dataset(self, cognite_client):
        feature_type_spec = ExperimentalFeatureType(
            external_id="external_id",
            data_set_id=4658488153688345,
            properties={f"attr{i}": {"type": "LONG"} for i in range(0, 80)},
        )
        try:
            cognite_client.geospatial.create_feature_types(feature_type_spec)
            raise pytest.fail("creating feature types with dataSetId should have raised an exception")
        except CogniteAPIError as e:
            assert e.message == "Unsupported field: dataSetId"

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

    def test_stream_features(self, cognite_client, test_feature_type, test_feature):
        features = cognite_client.geospatial.stream_features(
            feature_type_external_id=test_feature_type.external_id, filter={}
        )
        feature_list = FeatureList(list(features))
        assert len(feature_list) == 1

    def test_put_raster(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.put_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature.external_id,
            raster_property_name="raster",
            raster_format="XYZ",
            raster_srid=3857,
            file="tests/tests_integration/test_api/geospatial_data/raster-grid-example.xyz",
        )
        assert res.width == 4
        assert res.height == 5
        assert res.num_bands == 1
        assert res.scale_x == 1.0
        assert res.scale_y == 1.0
        assert res.skew_x == 0.0
        assert res.skew_y == 0.0
        assert res.srid == 3857
        assert res.upper_left_x == -0.5
        assert res.upper_left_y == -0.5

    def test_get_raster(self, cognite_client, test_feature_type, test_feature_with_raster):
        res = cognite_client.geospatial.get_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature_with_raster.external_id,
            raster_property_name="raster",
            raster_format="XYZ",
        )
        raster_content = open("tests/tests_integration/test_api/geospatial_data/raster-grid-example.xyz", "rb").read()
        assert res == raster_content

        res = cognite_client.geospatial.get_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature_with_raster.external_id,
            raster_property_name="raster",
            raster_format="XYZ",
            raster_options={"ADD_HEADER_LINE": "YES"},
        )
        raster_content = open(
            "tests/tests_integration/test_api/geospatial_data/raster-grid-header-example.xyz", "rb"
        ).read()
        assert res == raster_content

    def test_get_raster_with_transformation(self, cognite_client, test_feature_type, test_feature_with_raster):
        res = cognite_client.geospatial.get_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature_with_raster.external_id,
            raster_property_name="raster",
            raster_format="XYZ",
            raster_srid=54030,
            allow_crs_transformation=True,
        )
        raster_content = open(
            "tests/tests_integration/test_api/geospatial_data/raster-grid-54030-example.xyz", "rb"
        ).read()
        assert res == raster_content

    def test_retrieve_features_with_raster_property(self, cognite_client, test_feature_type, test_feature_with_raster):
        res = cognite_client.geospatial.retrieve_features(
            feature_type_external_id=test_feature_type.external_id,
            external_id=[test_feature_with_raster.external_id],
        )
        assert res[0].external_id == test_feature_with_raster.external_id
        raster_metadata = res[0].raster
        assert raster_metadata == {
            "width": 4,
            "height": 5,
            "numBands": 1,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "skewX": 0.0,
            "skewY": 0.0,
            "srid": 3857,
            "upperLeftX": -0.5,
            "upperLeftY": -0.5,
        }

    def test_put_raster_custom_crs(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.put_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature.external_id,
            raster_property_name="raster",
            raster_format="XYZ",
            raster_srid=54030,
            file="tests/tests_integration/test_api/geospatial_data/raster-grid-example.xyz",
            allow_crs_transformation=True,
        )
        assert res.width == 4
        assert res.height == 5
        assert res.num_bands == 1
        assert res.scale_x == 1.0
        assert res.scale_y == 1.0
        assert res.skew_x == 0.0
        assert res.skew_y == 0.0
        assert res.srid == 3857
        assert res.upper_left_x == -0.5891363261459447
        assert res.upper_left_y == -0.31623471547260973

    def test_delete_raster(self, cognite_client, test_feature_type, test_feature_with_raster):
        res = cognite_client.geospatial.delete_raster(
            feature_type_external_id=test_feature_type.external_id,
            feature_external_id=test_feature_with_raster.external_id,
            raster_property_name="raster",
        )
        assert res is None
        res = cognite_client.geospatial.retrieve_features(
            feature_type_external_id=test_feature_type.external_id,
            external_id=[test_feature_with_raster.external_id],
        )
        assert res[0].external_id == test_feature_with_raster.external_id
        assert hasattr(res[0], "raster") is False

    def test_delete_raster_property(self, cognite_client, test_feature_type, test_feature_with_raster):
        feature_type_updated = cognite_client.geospatial.update_feature_types(
            update=FeatureTypeUpdate(
                external_id=test_feature_type.external_id,
                add=PropertyAndSearchSpec(properties={}, search_spec={}),
                remove=PropertyAndSearchSpec(properties=["raster"], search_spec=[]),
            )
        )
        assert feature_type_updated[0].properties.keys() == {
            "pressure",
            "externalId",
            "lastUpdatedTime",
            "createdTime",
            "volume",
            "temperature",
            "position",
        }
        res = cognite_client.geospatial.retrieve_features(
            feature_type_external_id=test_feature_type.external_id,
            external_id=[test_feature_with_raster.external_id],
        )
        assert res[0].external_id == test_feature_with_raster.external_id
        assert hasattr(res[0], "raster") is False

    def test_get_mvt_mappings_definitions(self, cognite_client, test_mvt_mappings_def):
        res = cognite_client.geospatial.retrieve_mvt_mappings_definitions(external_id=test_mvt_mappings_def.external_id)
        assert res.external_id == test_mvt_mappings_def.external_id
        assert res.mappings[0]["levels"] == test_mvt_mappings_def.mappings[0]["levels"]
        assert res.mappings[0]["geometryProperty"] == test_mvt_mappings_def.mappings[0]["geometryProperty"]
        assert res.mappings[0]["featureProperties"] == test_mvt_mappings_def.mappings[0]["featureProperties"]

    def test_list_mvt_mappings_definitions(self, cognite_client, test_mvt_mappings_def):
        res = cognite_client.geospatial.list_mvt_mappings_definitions()
        assert len(res) == 1
        assert res[0].external_id == test_mvt_mappings_def.external_id

    def test_compute(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.compute(
            sub_computes={"geom1": {"ewkt": "SRID=4326;POLYGON Z((0 0 0,1 1 1,1 -1 1,0 0 0))"}},
            output={
                "polygonValue": {"ewkt": "SRID=4326;POLYGON Z((0 0 0,1 1 1,1 -1 1,0 0 0))"},
                "polygonFromRef": {"ref": "geom1"},
            },
        )
        assert type(res) == ComputedItemList
        assert len(res) == 1
        res = cognite_client.geospatial.compute(
            binary_output={
                "stAsGeotiff": {
                    "raster": {
                        "stAsRaster": {
                            "geometry": {"ewkt": "SRID=4326;POLYGON((0 0,4 6,10 10,0 0))"},
                            "width": 300,
                            "height": 200,
                        }
                    }
                }
            }
        )
        assert type(res) == bytes
        assert len(res) == 60426
        res = cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            filter={"equals": {"property": "externalId", "value": test_feature.external_id}},
            output={"mylocation": {"property": "position"}},
        )
        assert type(res) == ComputedItemList
