import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import TransformationDestination

COGNITE_CLIENT = CogniteClient()


class TestTransformationSchemaAPI:
    def test_assets(self):
        asset_columns = COGNITE_CLIENT.transformations.schema.retrieve(destination=TransformationDestination.assets())
        assert len(asset_columns) > 0 and len([col for col in asset_columns if col.name == "id"]) > 0
