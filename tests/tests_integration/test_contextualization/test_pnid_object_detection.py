import pytest
from cognite.client.data_classes import ContextualizationJob

PNID_FILE_ID = 3261066797848581


@pytest.fixture
def annotations_api(cognite_client):
    return cognite_client.legacy_annotations


@pytest.fixture
def pnid_object_detection_api(cognite_client):
    return cognite_client.pnid_object_detection


class TestPNIDObjectDetectionIntegration:
    def test_run_find_objects(self, pnid_object_detection_api):
        file_id = PNID_FILE_ID
        job = pnid_object_detection_api.find_objects(file_id)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items", "fileId"} == set(job.result.keys())
        assert "Completed" == job.status
        assert {"boundingBox", "score", "type"} == set(job.result["items"][0].keys())
