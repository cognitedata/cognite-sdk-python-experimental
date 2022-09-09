import os

import pytest
from cognite.client import ClientConfig
from cognite.client.credentials import APIKey, Token

from cognite.experimental import CogniteClient


class TestClient:
    def test_client(self):
        CogniteClient(
            ClientConfig(
                client_name="experimental",
                project="test",
                credentials=APIKey("test"),
            )
        )

    def test_client_token(self):
        CogniteClient(
            ClientConfig(
                client_name="experimental",
                project="test",
                credentials=Token("test"),
            )
        )
