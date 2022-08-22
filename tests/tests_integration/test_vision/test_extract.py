import pytest
from cognite.client.data_classes import FileMetadata
from cognite.client.data_classes.contextualization import JobStatus

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.vision import Feature, VisionExtractJob

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


@pytest.fixture(scope="class")
def file_id() -> int:
    return 2817345574340931


class TestExtract:
    def test_extract(self, file_id: int) -> None:
        job = VAPI.extract(features=Feature.PEOPLE_DETECTION, file_ids=[file_id])
        assert isinstance(job, VisionExtractJob)
        assert job.job_id > 0
        assert JobStatus(job.status) == JobStatus.QUEUED
        assert len(job.items) == 1
        assert job.items[0]["fileId"] == file_id
        assert job.status_time > 0
        assert job.created_time > 0
