import pytest

from cognite.client.data_classes import ContextualizationJob
from cognite.experimental import CogniteClient

COGNITE_CLIENT = CogniteClient()
PNID_OBJECT_DETECTION_API = COGNITE_CLIENT.pnid_object_detection
PNID_FILE_ID = 3261066797848581


class TestPNIDObjectDetectionIntegration:
    def test_run_find_objects(self):
        file_id = PNID_FILE_ID
        job = PNID_OBJECT_DETECTION_API.find_objects(file_id)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items", "fileId"} == set(job.result.keys())
        assert "Completed" == job.status
        assert {"boundingBox", "score", "type"} == set(job.result["items"][0].keys())
