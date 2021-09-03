import os
import uuid

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.geospatial import Feature, FeatureType

COGNITE_CLIENT = CogniteClient()
COGNITE_DISABLE_GZIP = "COGNITE_DISABLE_GZIP"


@pytest.fixture(params=[None, "smoke_test"])
def cognite_domain(request):
    yield request.param


@pytest.fixture()
def test_feature_type(cognite_domain):
    COGNITE_CLIENT.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = COGNITE_CLIENT.geospatial.create_feature_types(
        FeatureType(
            external_id=external_id, attributes={"temperature": {"type": "DOUBLE"}}, cognite_domain=cognite_domain
        )
    )
    yield feature_type
    COGNITE_CLIENT.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture()
def another_test_feature_type(cognite_domain):
    COGNITE_CLIENT.geospatial.set_current_cognite_domain(cognite_domain)
    external_id = f"FT_{uuid.uuid4().hex[:10]}"
    feature_type = COGNITE_CLIENT.geospatial.create_feature_types(
        FeatureType(external_id=external_id, attributes={"volume": {"type": "DOUBLE"}}, cognite_domain=cognite_domain)
    )
    yield feature_type
    COGNITE_CLIENT.geospatial.delete_feature_types(external_id=external_id)


@pytest.fixture
def test_feature(test_feature_type):
    external_id = f"F_{uuid.uuid4().hex[:10]}"
    feature = COGNITE_CLIENT.geospatial.create_features(
        test_feature_type, Feature(external_id=external_id, temperature=12.4)
    )
    yield feature
    COGNITE_CLIENT.geospatial.delete_features(test_feature_type, external_id=external_id)


@pytest.fixture
def another_test_feature(test_feature_type):
    external_id = f"F_{uuid.uuid4().hex[:10]}"
    feature = COGNITE_CLIENT.geospatial.create_features(
        test_feature_type, Feature(external_id=external_id, temperature=-10.8)
    )
    yield feature
    COGNITE_CLIENT.geospatial.delete_features(test_feature_type, external_id=external_id)


# we need to filter the old types based on their age, so setting autouse to false for now
@pytest.fixture(autouse=False, scope="module")
def clean_old_feature_types():
    for domain in [None, "smoke_test"]:
        COGNITE_CLIENT.geospatial.set_current_cognite_domain(domain)
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        for ft in res:
            print(f"Deleting old feature type {ft.external_id} in domain {'default' if domain is None else domain}")
            COGNITE_CLIENT.geospatial.delete_feature_types(external_id=ft.external_id)
    yield


@pytest.fixture(autouse=True, scope="module")
def disable_gzip():
    v = os.getenv(COGNITE_DISABLE_GZIP)
    os.environ[COGNITE_DISABLE_GZIP] = "true"
    yield
    if v is None:
        os.environ.pop(COGNITE_DISABLE_GZIP)
    else:
        os.environ[COGNITE_DISABLE_GZIP] = v


class TestGeospatialAPI:
    def test_retrieve_single_feature_type_by_external_id(self, cognite_domain, test_feature_type):
        assert (
            test_feature_type.external_id
            == COGNITE_CLIENT.geospatial.retrieve_feature_types(external_id=test_feature_type.external_id).external_id
        )
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_list_feature_types(self, cognite_domain, test_feature_type):
        res = COGNITE_CLIENT.geospatial.list_feature_types()
        assert 0 < len(res) < 100
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_retrieve_single_feature_by_external_id(self, cognite_domain, test_feature_type, test_feature):
        res = COGNITE_CLIENT.geospatial.retrieve_features(
            feature_type=test_feature_type, external_id=test_feature.external_id
        )
        assert res.external_id == test_feature.external_id
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_update_single_feature(self, cognite_domain, test_feature_type, test_feature):
        res = COGNITE_CLIENT.geospatial.update_features(
            feature_type=test_feature_type, feature=Feature(external_id=test_feature.external_id, temperature=6.237)
        )
        assert res.external_id == test_feature.external_id
        assert res.temperature == 6.237
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_search_features(self, cognite_domain, test_feature_type, test_feature):
        res = COGNITE_CLIENT.geospatial.search_features(
            feature_type=test_feature_type, filter={"range": {"attribute": "temperature", "gt": 12.0}}, limit=10
        )
        assert res[0].external_id == test_feature.external_id
        assert res[0].temperature == 12.4
        res = COGNITE_CLIENT.geospatial.search_features(
            feature_type=test_feature_type, filter={"range": {"attribute": "temperature", "lt": 12.0}}, limit=10
        )
        assert len(res) == 0
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_retrieve_multiple_feature_types_by_external_id(
        self, cognite_domain, test_feature_type, another_test_feature_type
    ):
        assert (
            len(
                COGNITE_CLIENT.geospatial.retrieve_feature_types(
                    external_id=[test_feature_type.external_id, another_test_feature_type.external_id]
                )
            )
            == 2
        )
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain

    def test_retrieve_multiple_features_by_external_id(
        self, cognite_domain, test_feature_type, test_feature, another_test_feature
    ):
        res = COGNITE_CLIENT.geospatial.retrieve_features(
            feature_type=test_feature_type, external_id=[test_feature.external_id, another_test_feature.external_id]
        )
        assert res[0].external_id == test_feature.external_id
        assert res[1].external_id == another_test_feature.external_id
        assert COGNITE_CLIENT.geospatial.get_current_cognite_domain() == cognite_domain
