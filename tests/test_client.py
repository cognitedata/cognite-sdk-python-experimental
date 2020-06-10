import os

import pytest

from cognite.experimental import CogniteClient


class TestClient:
    def test_client(self):
        CogniteClient(project="test", api_key="test")

    def test_client_token(self):
        CogniteClient(project="test", token="test")

    def test_client_auto_key(self):

        _environ = os.environ.copy()
        try:
            os.environ["TEST_API_KEY"] = ""
            os.environ["COGNITE_API_KEY"] = ""
            with pytest.raises(ValueError):
                CogniteClient(project="test")

            os.environ["TEST_API_KEY"] = "foo"
            CogniteClient(project="test")
        finally:
            os.environ.clear()
            os.environ.update(_environ)
