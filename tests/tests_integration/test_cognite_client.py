import os

import pytest
from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient

creds = OAuthClientCredentials(
    token_url=os.getenv("COGNITE_TOKEN_URL"),
    client_id=os.getenv("COGNITE_CLIENT_ID"),
    client_secret=os.getenv("COGNITE_CLIENT_SECRET"),
    scopes=[os.getenv("COGNITE_TOKEN_SCOPES")],
)
cnf = ClientConfig(
    client_name=os.getenv("COGNITE_CLIENT_NAME"),
    base_url=os.getenv("COGNITE_BASE_URL"),
    project=os.getenv("COGNITE_PROJECT"),
    credentials=creds,
)
c = CogniteClient(cnf)


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
