import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing
PNID_ID = 3261066797848581


class TestPNIDParsingIntegration:
    def test_run_detect(self):
        entities = ["a", "b"]
        file_id = PNID_ID
        job = PNIDAPI.detect(file_id, entities, name_mapping={"a": "c"}, partial_match=False, min_tokens=3)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items", "requestTimestamp", "startTimestamp", "statusTimestamp"} == set(job.result.keys())
        assert "Completed" == job.status

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
        file_id = PNID_ID
        job = PNIDAPI.convert(file_id, items=items, grayscale=True)
        assert isinstance(job, ContextualizationJob)
        assert {"pngUrl", "requestTimestamp", "startTimestamp", "statusTimestamp", "svgUrl"} == set(job.result.keys())
        assert "Completed" == job.status
