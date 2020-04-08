import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, ResourceTypingModel
from cognite.experimental.exceptions import ModelFailedException
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
RTAPI = COGNITE_CLIENT.resource_typing


@pytest.fixture
def mock_fit(rsps):
    response_body = {"modelId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST, RTAPI._get_base_url_with_base_path() + RTAPI._RESOURCE_PATH + "/fit", status=200, json=response_body
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"modelId": 123, "status": "Completed"}
    rsps.add(
        rsps.GET,
        re.compile(f"{RTAPI._get_base_url_with_base_path()}{RTAPI._RESOURCE_PATH}/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_failed(rsps):
    response_body = {"modelId": 123, "status": "Failed", "errorMessage": "error message"}
    rsps.add(
        rsps.GET,
        re.compile(f"{RTAPI._get_base_url_with_base_path()}{RTAPI._RESOURCE_PATH}/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestResourceTyping:
    def test_fit(self, mock_fit, mock_status_ok):
        items = [{"data": ["a", "b'"], "target": "x"}, {"data": ["c", "d'"], "target": "y"}]
        targets_to_classify = ["x"]

        model = RTAPI.fit(items, targets_to_classify=targets_to_classify)
        assert isinstance(model, ResourceTypingModel)
        assert "Queued" == model.status
        model.wait_for_completion()
        assert "Completed" == model.status
        assert 123 == model.model_id

        n_fit_calls = 0
        n_status_calls = 0
        for call in mock_fit.calls:
            if "fit" in call.request.url:
                n_fit_calls += 1
                assert {
                    "items": items,
                    "targetsToClassify": targets_to_classify,
                    "algorithm": "open_set_nearest_neighbors",
                } == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == n_fit_calls
        assert 1 == n_status_calls

    def test_fit_fails(self, mock_fit, mock_status_failed):
        model = RTAPI.fit([], [])
        with pytest.raises(ModelFailedException) as exc_info:
            model.wait_for_completion()
        assert exc_info.type is ModelFailedException
        assert 123 == exc_info.value.id
        assert "error message" == exc_info.value.error_message
        assert "ResourceTypingModel 123 failed with error 'error message'" == str(exc_info.value)

    def test_retrieve(self, mock_status_ok):
        model = RTAPI.retrieve(model_id=123)
        assert isinstance(model, ResourceTypingModel)
        assert "Completed" == model.status
        assert 123 == model.model_id
