import os
import uuid

import pytest
from cognite.client.data_classes.geospatial import *
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
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
                "position": {"type": "POINT", "srid": "4326", "optional": True},
                "volume": {"type": "DOUBLE", "optional": True},
                "temperature": {"type": "DOUBLE", "optional": True},
                "pressure": {"type": "DOUBLE", "optional": True},
                "raster": {"srid": 3857, "type": "RASTER", "storage": "embedded", "optional": True},
            },
            search_spec={"vol_press_idx": {"properties": ["volume", "pressure"]}},
        )
    )
    yield feature_type
    cognite_client.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture()
def test_partitioned_feature_type(cognite_client, cognite_domain):
    cognite_client.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = cognite_client.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id,
            properties={
                "position": {"type": "POINT", "srid": "4326", "optional": True},
                "volume": {"type": "DOUBLE", "optional": True},
                "temperature": {"type": "DOUBLE", "optional": True},
                "pressure": {"type": "DOUBLE", "optional": True},
                "raster": {"srid": 3857, "type": "RASTER", "storage": "embedded", "optional": True},
            },
            search_spec={"vol_press_idx": {"properties": ["volume", "pressure"]}},
            partitions=[{"from": "aa", "to": "ll"}, {"from": "ll", "to": "zz"}],
        )
    )
    yield feature_type
    cognite_client.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture()
def test_into_feature_type(cognite_client, cognite_domain):
    cognite_client.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = cognite_client.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id,
            properties={
                "position": {"type": "POINT", "srid": "4326", "optional": True},
                "volume": {"type": "DOUBLE", "optional": True},
                "temperature": {"type": "DOUBLE", "optional": True},
                "pressure": {"type": "DOUBLE", "optional": True},
                "raster": {"srid": 3857, "type": "RASTER", "storage": "embedded", "optional": True},
            },
            search_spec={"vol_press_idx": {"properties": ["volume", "pressure"]}},
        )
    )
    yield feature_type
    cognite_client.geospatial.delete_feature_types(external_id=external_id, recursive=True)


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


@pytest.fixture()
def test_feature_type_with_reference(cognite_client, cognite_domain):
    cognite_client.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = cognite_client.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id,
            properties={
                "myRef": {"type": "STRING", "size": 32},
                "speed": {"type": "DOUBLE"},
            },
        )
    )
    yield feature_type
    cognite_client.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture
def test_feature_with_reference(cognite_client, test_feature_type_with_reference, test_feature):
    external_id = f"F/O@ö_{uuid.uuid4().hex[:10]}"
    feature = cognite_client.geospatial.create_features(
        test_feature_type_with_reference.external_id,
        Feature(
            external_id=external_id,
            myRef=test_feature.external_id,
            speed=99.9,
        ),
    )
    yield feature
    cognite_client.geospatial.delete_features(test_feature_type_with_reference.external_id, external_id=external_id)


@pytest.fixture
def test_session_nonce(cognite_client):
    session = cognite_client.iam.sessions.create()
    yield session.nonce


@pytest.fixture
def test_task(cognite_client, test_feature_type, test_session_nonce):
    task = cognite_client.geospatial.create_tasks(
        session_nonce=test_session_nonce,
        task=GeospatialTask(
            external_id=f"task_{uuid.uuid4().hex[:10]}",
            task_type="FEATURES_INGESTION",
            request={
                "fileExternalId": "somefile.csv",
                "intoFeatureType": test_feature_type.external_id,
                "columns": ["_external_id", "tag"],
                "recreateIndex": False,
            },
        ),
    )
    yield task


class TestExperimentalGeospatialAPI:
    @pytest.mark.skip(reason="test fails with error 400 'Data sets do not exist.'")
    def test_create_feature_type_dataset(self, cognite_client):
        feature_type_spec = FeatureType(
            external_id="external_id",
            data_set_id=4658488153688345,
            properties={f"attr{i}": {"type": "LONG"} for i in range(0, 80)},
        )
        try:
            cognite_client.geospatial.create_feature_types(feature_type_spec)
            raise pytest.fail("creating feature types with dataSetId should have raised an exception")
        except CogniteAPIError as e:
            assert e.message == "Unsupported field: dataSetId"

    def test_create_partitioned_feature_type(self, cognite_client, test_partitioned_feature_type):
        assert len(test_partitioned_feature_type.partitions) == 2
        assert test_partitioned_feature_type.partitions[0] == {"from": "aa", "to": "ll"}
        assert test_partitioned_feature_type.partitions[1] == {"from": "ll", "to": "zz"}

    def test_list_feature_types(self, cognite_client, test_partitioned_feature_type):
        res = cognite_client.geospatial.list_feature_types()
        assert 0 < len(res) < 100
        assert res[-1].partitions[0] == {"from": "aa", "to": "ll"}
        assert res[-1].partitions[1] == {"from": "ll", "to": "zz"}

    def test_retrieve_single_feature_type_by_external_id(self, cognite_client, test_partitioned_feature_type):
        res = cognite_client.geospatial.retrieve_feature_types(external_id=test_partitioned_feature_type.external_id)
        assert test_partitioned_feature_type.external_id == res.external_id
        assert res.partitions[0] == {"from": "aa", "to": "ll"}
        assert res.partitions[1] == {"from": "ll", "to": "zz"}

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

    def test_upsert_features(self, cognite_client, test_feature_type):
        external_id = f"F_{uuid.uuid4().hex[:10]}"
        feature = Feature(
            external_id=external_id,
            position={"wkt": "POINT(50 50)"},
            temperature=12.4,
            volume=1212.0,
            pressure=2121.0,
        )
        cognite_client.geospatial.upsert_features(test_feature_type.external_id, feature)
        cognite_client.geospatial.upsert_features(test_feature_type.external_id, feature)
        cognite_client.geospatial.delete_features(test_feature_type.external_id, external_id=external_id)

    def test_stream_features(self, cognite_client, test_feature_type, test_feature):
        features = cognite_client.geospatial.stream_features(
            feature_type_external_id=test_feature_type.external_id, filter={}
        )
        feature_list = FeatureList(list(features))
        assert len(feature_list) == 1

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

    def test_compute_sub_computes(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.compute(
            sub_computes={"geom1": {"output": {"ewkt": "SRID=4326;POLYGON Z((0 0 0,1 1 1,1 -1 1,0 0 0))"}}},
            output={
                "polygonValue": {"ewkt": "SRID=4326;POLYGON Z((0 0 0,1 1 1,1 -1 1,0 0 0))"},
                "polygonFromRef": {"ref": "ewkt", "source": "geom1"},
            },
        )
        assert type(res) == ComputedItemList
        assert len(res) == 1

    def test_compute_binary_output(self, cognite_client, test_feature_type, test_feature):
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

    def test_compute_from_feature_type(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            filter={"equals": {"property": "externalId", "value": test_feature.external_id}},
            output={"mylocation": {"property": "position"}},
        )
        assert type(res) == ComputedItemList

    def test_compute_into_feature_type(self, cognite_client, test_feature_type, test_into_feature_type, test_feature):
        cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            output={"externalId": {"property": "externalId"}},
            into_feature_type=test_into_feature_type.external_id,
        )

    def test_compute_group_by(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            group_by=[{"property": "volume"}],
            output={"count": {"count": {"property": "temperature"}}, "volume": {"property": "volume"}},
        )
        assert type(res) == ComputedItemList

    def test_compute_order_by(self, cognite_client, test_feature_type, test_feature):
        res = cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            order_by=[ComputeOrder({"property": "volume"}, "ASC")],
            output={"volume": {"property": "volume"}},
        )
        assert type(res) == ComputedItemList

    def test_compute_left_joins(
        self,
        cognite_client,
        test_feature_type,
        test_feature_type_with_reference,
        test_feature,
        test_feature_with_reference,
    ):
        res = cognite_client.geospatial.compute(
            from_feature_type=test_feature_type.external_id,
            left_joins=[
                {
                    "featureType": test_feature_type_with_reference.external_id,
                    "condition": {
                        "equals": {
                            "expr1": {"featureType": test_feature_type.external_id, "property": "externalId"},
                            "expr2": {"featureType": test_feature_type_with_reference.external_id, "property": "myRef"},
                        },
                    },
                }
            ],
            output={
                "ext1": {"featureType": test_feature_type_with_reference.external_id, "property": "externalId"},
                "speed": {"featureType": test_feature_type_with_reference.external_id, "property": "speed"},
                "extRef": {"featureType": test_feature_type_with_reference.external_id, "property": "myRef"},
                "volume": {"featureType": test_feature_type.external_id, "property": "volume"},
            },
        )
        assert type(res) == ComputedItemList

    @pytest.mark.skip(reason="tasks are only deployed in azure-dev")
    def test_create_tasks(self, test_task):
        assert test_task.task_type == "FEATURES_INGESTION"

    @pytest.mark.skip(reason="tasks are only deployed in azure-dev")
    def test_get_tasks(self, cognite_client, test_task):
        res = cognite_client.geospatial.get_tasks(external_id=test_task.external_id)
        assert res.task_type == "FEATURES_INGESTION"
        assert res.external_id == test_task.external_id
