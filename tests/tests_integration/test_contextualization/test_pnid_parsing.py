import pytest
from cognite.client.data_classes import ContextualizationJob

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import PNIDDetectionList, PNIDDetectionPageList

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing
PNID_FILE_ID = 3261066797848581


@pytest.mark.skip(reason="This test fails approx 4 out of 5 times")
class TestPNIDParsingIntegration:
    def test_run_detect_str(self):
        entities = ["YT-96122", "XE-96125"]
        file_id = PNID_FILE_ID
        job = PNIDAPI.detect(file_id=file_id, entities=entities)
        assert isinstance(job, ContextualizationJob)
        assert {"items", "fileId", "fileExternalId"} == set(job.result.keys())
        assert "Completed" == job.status

        assert isinstance(job._repr_html_(), str)
        assert isinstance(job.matches, PNIDDetectionList)

    def test_run_detect_entities_dict(self):
        entities = [{"name": "YT-96122"}, {"name": "XE-96125", "ee": 123}, {"name": "XWDW-9615"}]
        file_id = PNID_FILE_ID
        job = PNIDAPI.detect(file_id=file_id, entities=entities)
        assert isinstance(job, ContextualizationJob)
        assert {"items", "fileId", "fileExternalId"} == set(job.result.keys())
        assert "Completed" == job.status
        ocr_result = PNIDAPI.ocr(file_id=file_id)
        assert isinstance(ocr_result, PNIDDetectionPageList)
        assert isinstance(ocr_result._repr_html_(), str)
        assert 1 == len(ocr_result)
        assert isinstance(ocr_result[0], PNIDDetectionList)
        assert isinstance(ocr_result[0]._repr_html_(), str)

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
        job = PNIDAPI.convert(file_id=file_id, items=items, grayscale=True)
        assert isinstance(job, ContextualizationJob)
        assert {
            "pngUrl",
            "svgUrl",
            "fileId",
            "fileExternalId",
        } == set(job.result.keys())
        assert "Completed" == job.status
