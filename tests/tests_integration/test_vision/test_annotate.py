import pytest
from cognite.client.data_classes import FileMetadata
from cognite.client.data_classes.contextualization import JobStatus

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.vision import AnnotateJobResults, Feature

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


@pytest.fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient()


# TODO(VIS-986): replace this file generator with a hard-coded ID of an actual image
@pytest.fixture(scope="class")
def file_id(cognite_client: CogniteClient) -> int:
    # Create a test file
    name = "vision_annotate_test_file"
    file = cognite_client.files.create(FileMetadata(external_id=name, name=name), overwrite=True)[0]
    yield file.id

    cognite_client.files.delete(id=file.id)


class TestAssetDetection:
    def test_asset_detection(self, file_id: int) -> None:
        job = VAPI.annotate(features=Feature.PEOPLE_DETECTION, file_ids=[file_id])
        assert isinstance(job, AnnotateJobResults)
        assert job.job_id > 0
        assert JobStatus(job.status) == JobStatus.QUEUED
        assert len(job.items) == 1
        assert job.items[0]["fileId"] == file_id
        assert job.status_time > 0
        assert job.created_time > 0