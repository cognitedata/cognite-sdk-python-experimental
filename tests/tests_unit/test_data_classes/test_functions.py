from unittest.mock import MagicMock

import pytest

from cognite.experimental.data_classes import Function


@pytest.fixture
def empty_function():
    return Function(id=123, cognite_client=MagicMock())


@pytest.fixture
def function():
    return Function(
        id=123,
        name="my-function",
        description="some description",
        owner="somebody",
        status="Deploying",
        file_id=456,
        created_time="2020-06-19 08:49:37",
        secrets={},
        cognite_client=MagicMock(),
    )


class TestFunction:
    def test_update(self, empty_function, function):
        empty_function._cognite_client.functions.retrieve.return_value = function

        empty_function.update()
        assert function == empty_function

    def test_update_on_deleted_function(self, empty_function):
        empty_function._cognite_client.functions.retrieve.return_value = None
        empty_function.update()
