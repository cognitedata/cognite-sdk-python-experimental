import pytest
from cognite.client.data_classes import ContextualizationJob

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import PNIDDetectionList, PNIDDetectionPageList

COGNITE_CLIENT = CogniteClient()
DIAGRAMSAPI = COGNITE_CLIENT.diagrams
PNID_FILE_ID = 3261066797848581


class TestPNIDParsingIntegration:
    def test_run_detect_entities_dict(self):
        entities = [{"name": "YT-96122"}, {"name": "XE-96125", "ee": 123}, {"name": "XWDW-9615"}]
        file_id = PNID_FILE_ID
        job = DIAGRAMSAPI.detect(file_ids=[file_id], entities=entities)
        assert isinstance(job, ContextualizationJob)
        print(job.result)
        assert {"items", "partialMatch", "minTokens", "searchField"} == set(job.result.keys())
        assert {"fileId", "results"} == job.result["items"][0].keys()
        assert "Completed" == job.status

        convert_job = job.convert()

        assert isinstance(convert_job, ContextualizationJob)
        assert {"items"} == set(convert_job.result.keys())
        assert {"pngUrl", "svgUrl", "fileId", "fileExternalId"} == set(convert_job.result["items"][0].keys())
        assert "Completed" == job.status
