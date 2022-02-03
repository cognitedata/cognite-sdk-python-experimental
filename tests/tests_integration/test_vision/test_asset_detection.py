from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    EntityMatchingMatchList,
    EntityMatchingPipeline,
    EntityMatchingPipelineRunList,
    EntityMatchingPipelineUpdate,
)
from cognite.experimental.data_classes.vision import JobStatus

COGNITE_CLIENT = CogniteClient()
VAPI = COGNITE_CLIENT.vision


class TestAssetDetection:
    def test_create_job(self):
        # by providing a unknown file id, we expect the service to return 400 not found
        # otherwise we can assume the 400 error relates to invalid json fields.
        # There is no need to test internal behavior of the vision service, just verify the request structure.

        NON_EXISTENT_FILE_ID = 2
        try:
            response = VAPI.detect_assets_in_files(files=[NON_EXISTENT_FILE_ID])
        except CogniteAPIError as e:
            if e.code == 400 and e.missing is not None:
                response = None
                pass
            else:
                raise

        assert response is not None
        assert response.job_id > 0
        assert response.status == JobStatus.QUEUED
        assert len(response.items) == 1
        assert response.items[0].file_id == NON_EXISTENT_FILE_ID
        assert response.status_time > 0
        assert response.created_time > 0
        assert response.start_time > 0
