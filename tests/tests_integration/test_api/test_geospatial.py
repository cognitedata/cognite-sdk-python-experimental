from cognite.experimental import CogniteClient

COGNITE_CLIENT = CogniteClient()


class TestGeospatialAPI:
    def test_create_feature_type(self):
        res = COGNITE_CLIENT.geospatial.create_feature_type(
            external_id="my_feature_type", attributes={"temperature": {"type": "DOUBLE"}}
        )
        COGNITE_CLIENT.geospatial.delete_feature_type(external_id="my_feature_type")
        print(res)
