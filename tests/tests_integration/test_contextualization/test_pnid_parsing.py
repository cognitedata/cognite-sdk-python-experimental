import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing
PNID_FILE_ID = 3261066797848581


class TestPNIDParsingIntegration:
    def test_run_detect_str(self):
        entities = ["YT-96122", "XE-96125"]
        file_id = PNID_FILE_ID
        job = PNIDAPI.detect(file_id, entities)
        assert isinstance(job, ContextualizationJob)
        assert "Completed" == job.status  # the job is completed in the PNIDParsingAPI
        assert {"items", "requestTimestamp", "startTimestamp", "statusTimestamp"} == set(job.result.keys())

    def test_run_detect_entities_dict(self):
        entities = [{"name": "YT-96122"}, {"name": "XE-96125", "ee": 123}, {"name": "XWDW-9615"}]
        file_id = PNID_FILE_ID
        job = PNIDAPI.detect(file_id, entities)
        assert isinstance(job, ContextualizationJob)
        assert "Completed" == job.status  # the job is completed in the PNIDParsingAPI
        assert {"items", "requestTimestamp", "startTimestamp", "statusTimestamp"} == set(job.result.keys())

    def test_run_convert(self):
        items = [
            {
                "text": "21-PT-1019",
                "boundingBox": {
                    "xMax": 0.5895183277794608,
                    "xMin": 0.573159648591336,
                    "yMax": 0.3737254901960784,
                    "yMin": 0.3611764705882352,
                },
            }
        ]
        file_id = PNID_FILE_ID
        job = PNIDAPI.convert(file_id, items=items, grayscale=True)
        assert isinstance(job, ContextualizationJob)
        assert {"pngUrl", "requestTimestamp", "startTimestamp", "statusTimestamp", "svgUrl"} == set(job.result.keys())
        assert "Completed" == job.status
