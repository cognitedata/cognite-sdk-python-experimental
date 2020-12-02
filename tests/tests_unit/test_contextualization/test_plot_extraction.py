import re

import pytest

from cognite.client.data_classes import ContextualizationJob
from cognite.client.exceptions import ModelFailedException
from cognite.experimental import CogniteClient
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
PDAPI = COGNITE_CLIENT.plot_extraction


@pytest.fixture
def mock_complete(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        PDAPI._get_base_url_with_base_path() + PDAPI._RESOURCE_PATH + "/extractdata",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed", "items": []}
    rsps.add(
        rsps.GET,
        re.compile(PDAPI._get_base_url_with_base_path() + PDAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestPlotDataExtraction:
    def test_extract(self, mock_complete, mock_status_ok):

        job = PDAPI.extract(image="foo", plot_axes={"xMin": 0, "xMax": 1, "yMin": 0, "yMax": 1})
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items": []} == job.result
        assert "Completed" == job.status
        assert 123 == job.job_id

        extract_calls = 0
        n_status_calls = 0
        for call in mock_complete.calls:
            if call.request.method == "POST":
                extract_calls += 1
                assert {"plotImage": "foo", "plotAxes": {"xMin": 0, "xMax": 1, "yMin": 0, "yMax": 1}} == jsgz_load(
                    call.request.body
                )
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls
