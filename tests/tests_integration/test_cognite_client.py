import os

import pytest
from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient

c = CogniteClient(
    ClientConfig(
        client_name=os.environ["COGNITE_CLIENT_NAME"],
        project="Experimental cognite client",
        base_url=os.getenv("COGNITE_BASE_URL"),
        credentials=OAuthClientCredentials(
            client_id=os.environ["COGNITE_CLIENT_ID"],
            client_secret=os.environ["COGNITE_CLIENT_SECRET"],
            token_url=os.environ["COGNITE_TOKEN_URL"],
            scopes=os.getenv("COGNITE_TOKEN_SCOPES", "").split(","),
        ),
    )
)


class TestCogniteClient:
    def test_get(self):
        res = c.get("/login/status")
        assert res.status_code == 200

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
