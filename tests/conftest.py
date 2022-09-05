import os
import re

import pytest
import responses
from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.geospatial import *

from cognite.experimental._client import CogniteClient
from cognite.experimental.data_classes import Annotation, AnnotationFilter


@pytest.fixture
def annotation() -> Annotation:
    return Annotation(
        annotation_type="diagrams.FileLink",
        data={
            "fileRef": {"id": 1, "externalId": None},
            "pageNumber": 1,
            "textRegion": {
                "xMin": 0.0,
                "xMax": 0.5,
                "yMin": 0.5,
                "yMax": 1.0,
            },
        },
        status="approved",
        creating_app="UnitTest",
        creating_app_version="0.0.1",
        creating_user=None,
        annotated_resource_type="file",
        annotated_resource_id=1,
        annotated_resource_external_id=None,
    )


@pytest.fixture
def annotation_filter() -> AnnotationFilter:
    return AnnotationFilter(
        annotated_resource_type="file",
        annotated_resource_ids=[{"id": 1234}, {"external_id": "ext_1234"}],
        annotation_type="diagrams.FileLink",
        status="approved",
        creating_app="UnitTest",
        creating_user="",
        creating_app_version="0.0.1",
    )


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


@pytest.fixture(scope="class")
def cognite_client() -> CogniteClient:
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
    return CogniteClient(cnf)
