from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.geospatial import FeatureType

COGNITE_CLIENT = CogniteClient()


class TestGeospatialAPI:
    def test_create_feature_types(self):
        try:
            COGNITE_CLIENT.geospatial.delete_feature_type(external_id="my_feature_type")
        except:
            pass
        res = COGNITE_CLIENT.geospatial.create_feature_types(
            FeatureType(external_id="my_feature_type", attributes={"temperature": {"type": "DOUBLE"}})
        )
        COGNITE_CLIENT.geospatial.delete_feature_type(external_id="my_feature_type")
        print(res)
