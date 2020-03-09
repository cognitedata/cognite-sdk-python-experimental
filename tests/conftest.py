import os

import pytest
import responses


@pytest.fixture
def rsps():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def disable_gzip():
    os.environ["COGNITE_DISABLE_GZIP"] = "1"
    yield
    del os.environ["COGNITE_DISABLE_GZIP"]
