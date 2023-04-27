import pytest
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient

c = CogniteClient()


class TestCogniteClient:
    def test_get(self):
        with pytest.raises(CogniteAPIError) as e:
            c.get("/login")
        assert e.value.code == 404

    def test_post(self):
        with pytest.raises(CogniteAPIError) as e:
            c.post("/login", json={})
        assert e.value.code == 404

    def test_put(self):
        with pytest.raises(CogniteAPIError) as e:
            c.put("/login")
        assert e.value.code == 404

    def test_delete(self):
        with pytest.raises(CogniteAPIError) as e:
            c.delete("/login")
        assert e.value.code == 404
