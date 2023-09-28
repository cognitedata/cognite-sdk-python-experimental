import os
import uuid
from time import sleep

import pytest
from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    HostedExtractorsDestination,
    HostedExtractorsJob,
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
        jobs = [j for j in cognite_client.hosted_extractors.jobs.list() if j.external_id.startswith(test_id)]
        cognite_client.hosted_extractors.jobs.delete([j.external_id for j in jobs])
    except:
        pass

    try:
        sources = [s for s in cognite_client.hosted_extractors.sources.list() if s.external_id.startswith(test_id)]
        cognite_client.hosted_extractors.sources.delete([s.external_id for s in sources])
    except:
        pass

    try:
        destinations = [
            d for d in cognite_client.hosted_extractors.destinations.list() if d.external_id.startswith(test_id)
        ]
        cognite_client.hosted_extractors.destinations.delete([d.external_id for d in destinations])
    except:
        pass


@pytest.fixture()
def create_source(cognite_client: CogniteClient):
    yield cognite_client.hosted_extractors.sources.create(
        HostedExtractorsMqttSource(
            external_id=f"{test_id}-test-helper-source",
            type="mqtt3",
            host="mqtt.pluto-test.cognite.ai",
            use_tls=True,
            username="user",
            password="pass",
        ),
    )
    cognite_client.hosted_extractors.sources.delete(
        f"{test_id}-test-helper-source", force=True, ignore_unknown_ids=True
    )


@pytest.fixture()
def create_destination(cognite_client: CogniteClient):
    yield cognite_client.hosted_extractors.destinations.create(
        HostedExtractorsDestination(
            external_id=f"{test_id}-test-helper-dest",
        ),
    )
    cognite_client.hosted_extractors.destinations.delete(
        f"{test_id}-test-helper-dest", force=True, ignore_unknown_ids=True
    )


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
def test_source_crud(cognite_client: CogniteClient, source: HostedExtractorsSource):
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

    cognite_client.hosted_extractors.sources.delete(source.external_id)

    after_delete = cognite_client.hosted_extractors.sources.list()
    for s in after_delete:
        if s.external_id == source.external_id:
            assert False, "source still exists after deletion"


good_jobs = [
    HostedExtractorsJob(
        f"{test_id}-test-1",
        format={"type": "cognite"},
        config={"topicFilter": "#"},
        source_id=f"{test_id}-test-helper-source",
        destination_id=f"{test_id}-test-helper-dest",
    ),
    HostedExtractorsJob(
        f"{test_id}-test-2",
        format={"type": "rockwell", "prefix": {"prefix": "heyoo"}},
        config={"topicFilter": "#"},
        source_id=f"{test_id}-test-helper-source",
        destination_id=f"{test_id}-test-helper-dest",
    ),
]

bad_jobs = [
    HostedExtractorsJob(
        f"{test_id}-test-1",
        format={"type": "cognite"},
        config={"topicFilter": "#"},
        source_id="no-such-source",
        destination_id=f"{test_id}-test-helper-dest",
    ),
    HostedExtractorsJob(
        f"{test_id}-test-1",
        format={"type": "cognite"},
        source_id=f"{test_id}-test-helper-source",
        destination_id=f"{test_id}-test-helper-dest",
    ),
]


@pytest.mark.parametrize("job", good_jobs)
def test_job_crud(cognite_client: CogniteClient, create_source, create_destination, job):
    existing_jobs = cognite_client.hosted_extractors.jobs.list()
    for j in existing_jobs:
        if j.external_id == job.external_id:
            assert False, "job already exists"

    cognite_client.hosted_extractors.jobs.create(job)

    new_jobs = cognite_client.hosted_extractors.jobs.list()
    created_job = None
    for j in new_jobs:
        if j.external_id == job.external_id:
            created_job = j

    if not created_job:
        assert False, "job was not created"

    assert job.external_id == created_job.external_id

    cognite_client.hosted_extractors.jobs.delete(job.external_id)

    after_delete = cognite_client.hosted_extractors.jobs.list()
    for j in after_delete:
        if j.external_id == job.external_id:
            assert False, "job still exists after deletion"


@pytest.mark.parametrize("job", bad_jobs)
def test_create_bad_jobs(cognite_client: CogniteClient, create_source, create_destination, job):
    with pytest.raises(CogniteAPIError):
        cognite_client.hosted_extractors.jobs.create(job)


def test_force_delete_source(cognite_client, create_source, create_destination):
    cognite_client.hosted_extractors.jobs.create(good_jobs[0])

    with pytest.raises(CogniteAPIError):
        cognite_client.hosted_extractors.sources.delete(create_source.external_id)

    cognite_client.hosted_extractors.sources.delete(create_source.external_id, force=True)

    jobs_after_delete = cognite_client.hosted_extractors.jobs.list()
    for j in jobs_after_delete:
        if j.external_id == good_jobs[0].external_id:
            assert False, "job still exists after force deleting source"

    sources_after_delete = cognite_client.hosted_extractors.sources.list()
    for s in sources_after_delete:
        if s.external_id == create_source.external_id:
            assert False, "source still exists after force deleting"


def test_ignore_delete_source(cognite_client, create_source):
    with pytest.raises(CogniteAPIError):
        cognite_client.hosted_extractors.sources.delete([create_source.external_id, "doesnt-exist"])

    cognite_client.hosted_extractors.sources.delete(
        [create_source.external_id, "doesnt-exist"], ignore_unknown_ids=True
    )

    sources_after_delete = cognite_client.hosted_extractors.sources.list()
    for s in sources_after_delete:
        if s.external_id == create_source.external_id:
            assert False, "source still exists after force deleting"
