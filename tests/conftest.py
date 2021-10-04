import os
import re

import pytest
import responses


@pytest.fixture
def rsps():
    with responses.RequestsMock() as rsps:
        rsps.add(
            rsps.POST,
            re.compile("https://login.microsoftonline.com.*"),
            status=200,
            json={"token_type": "Bearer", "expires_in": 3599, "ext_expires_in": 3599, "access_token": "a.b.c"},
        )
        rsps.assert_all_requests_are_fired = False
        yield rsps


@pytest.fixture
def disable_gzip():
    os.environ["COGNITE_DISABLE_GZIP"] = "1"
    yield
    del os.environ["COGNITE_DISABLE_GZIP"]
