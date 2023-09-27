import os
import uuid

import pytest
from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    HostedExtractorsKafkaSource,
    HostedExtractorsMqttSource,
    HostedExtractorsRestSource,
    HostedExtractorsSource,
)

test_id = str(uuid.uuid4())


@pytest.fixture()
def cognite_client() -> CogniteClient:
    return CogniteClient(
        config=ClientConfig(
            base_url=os.environ["COGNITE_BASE_URL"],
            client_name="experimental-sdk-tests",
            project=os.environ["COGNITE_PROJECT"],
            credentials=OAuthClientCredentials(
                token_url=os.environ["COGNITE_TOKEN_URL"],
                client_id=os.environ["COGNITE_CLIENT_ID"],
                client_secret=os.environ["COGNITE_CLIENT_SECRET"],
                scopes=os.environ["COGNITE_TOKEN_SCOPES"].split(","),
            ),
        )
    )


@pytest.fixture()
def cleanup(cognite_client: CogniteClient):
    yield

    try:
        sources = [s for s in cognite_client.hosted_extractors.sources.list() if s.external_id.startswith(test_id)]
        cognite_client.hosted_extractors.sources.delete([s.external_id for s in sources])
    except:
        pass


good_sources = [
    HostedExtractorsRestSource(external_id=f"{test_id}-test-rest", type="rest", host="https://nrk.no", interval="1h"),
    HostedExtractorsMqttSource(
        external_id=f"{test_id}-test-mqtt",
        type="mqtt3",
        host="mqtt.pluto-test.cognite.ai",
        use_tls=True,
        username="user",
        password="pass",
    ),
    HostedExtractorsKafkaSource(
        external_id=f"{test_id}-test-kafka", type="kafka", host=["kafka.pluto-test.cognite.ai"], username="abc123"
    ),
]


@pytest.mark.parametrize("source", good_sources)
def test_create_read_delete_source(cognite_client: CogniteClient, cleanup, source: HostedExtractorsSource):
    existing_sources = cognite_client.hosted_extractors.sources.list()
    for s in existing_sources:
        if s.external_id == source.external_id:
            assert False, "source already exists"

    cognite_client.hosted_extractors.sources.create(source)

    new_sources = cognite_client.hosted_extractors.sources.list()
    created_source = None
    for s in new_sources:
        if s.external_id == source.external_id:
            created_source = s

    if not created_source:
        assert False, "source was not created"

    assert source.type == created_source.type
    assert source.host == created_source.host
    assert source.external_id == created_source.external_id
