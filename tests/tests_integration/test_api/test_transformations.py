import time
from unittest import mock

import pytest
from cognite.client import utils
from cognite.client.exceptions import CogniteAPIError, CogniteNotFoundError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Transformation
from cognite.experimental.data_classes.transformations import TransformationDestination
from tests.utils import set_request_limit

COGNITE_CLIENT = CogniteClient()


@pytest.fixture
def new_transformation():
    transform = Transformation(name="any", destination=TransformationDestination.Raw("", ""))
    ts = COGNITE_CLIENT.transformations.create(transform)

    yield ts

    COGNITE_CLIENT.transformations.delete(id=ts.id)
    assert COGNITE_CLIENT.transformations.retrieve(ts.id) is None


class TestTransformationsAPI:
    def test_create(self, new_transformation):
        assert (
            new_transformation.name == "any"
            and new_transformation.destination.type == "raw_table"
            and new_transformation.destination.rawType == "plain_raw"
            and new_transformation.id is not None
        )

    def test_retrieve(self, new_transformation):
        retrieved_transformation = COGNITE_CLIENT.transformations.retrieve(new_transformation.id)
        assert (
            new_transformation.name == retrieved_transformation.name
            and new_transformation.destination.type == retrieved_transformation.destination.type
            and new_transformation.id == retrieved_transformation.id
        )

    def test_list(self, new_transformation):
        retrieved_transformations = COGNITE_CLIENT.transformations.list()
        assert new_transformation.id in [transformation.id for transformation in retrieved_transformations]
