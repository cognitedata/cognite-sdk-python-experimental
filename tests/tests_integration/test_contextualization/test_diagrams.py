from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import DiagramConvertResults, DiagramDetectItem, DiagramDetectResults

COGNITE_CLIENT = CogniteClient()
DIAGRAMSAPI = COGNITE_CLIENT.diagrams
PNID_FILE_ID = 3261066797848581


class TestPNIDParsingIntegration:
    def test_run_detect_entities_dict(self):
        entities = [{"name": "YT-96122"}, {"name": "XE-96125", "ee": 123}, {"name": "XWDW-9615"}]
        file_id = PNID_FILE_ID
        job = DIAGRAMSAPI.detect(file_ids=[file_id], entities=entities)
        assert isinstance(job, DiagramDetectResults)
        assert {"items", "partialMatch", "minTokens", "searchField"} == set(job.result.keys())
        assert {"fileId", "annotations"} == job.result["items"][0].keys()
        assert "Completed" == job.status
        assert [] == job.errors
        assert isinstance(job.items[0], DiagramDetectItem)
        assert isinstance(job[PNID_FILE_ID], DiagramDetectItem)

        assert 2 == len(job[PNID_FILE_ID].annotations)
        for annotation in job[PNID_FILE_ID].annotations:
            assert 1 == annotation["region"]["page"]

        convert_job = job.convert()

        assert isinstance(convert_job, DiagramConvertResults)
        assert {"items", "grayscale"} == set(convert_job.result.keys())
        assert {"results", "fileId", "fileExternalId"} == set(convert_job.result["items"][0].keys())
        assert {"pngUrl", "svgUrl", "page"} == set(convert_job.result["items"][0]["results"][0].keys())
        assert "Completed" == convert_job.status

        for res_page in convert_job[PNID_FILE_ID].pages:
            assert 1 == res_page.page
            assert ".svg" in res_page.svg_url
            assert ".png" in res_page.png_url
