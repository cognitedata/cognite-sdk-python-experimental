import re

import pytest

from cognite.client.data_classes import ContextualizationJob
from cognite.experimental import CogniteClient
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
SCAPI = COGNITE_CLIENT.templates.completion


@pytest.fixture
def mock_complete_type(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/type",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_complete_template(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/template",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_suggest_instance(rsps):
    response_body = {"jobId": 123, "status": "Queued"}
    rsps.add(
        rsps.POST,
        SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/instancesuggestion",
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed", "items": []}
    rsps.add(
        rsps.GET,
        re.compile(SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


@pytest.fixture
def mock_suggest_instance_status_ok(rsps):
    response_body = {"jobId": 123, "status": "Completed", "items": []}
    rsps.add(
        rsps.GET,
        re.compile(SCAPI._get_base_url_with_base_path() + SCAPI._RESOURCE_PATH + "/instancesuggestion/\\d+"),
        status=200,
        json=response_body,
    )
    yield rsps


class TestSchemaCompletion:
    def test_complete_type(self, mock_complete_type, mock_status_ok):
        eid = "schematocomplete"
        job = SCAPI.complete_type(external_id=eid)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items": []} == job.result
        assert "Completed" == job.status
        assert 123 == job.job_id

        extract_calls = 0
        n_status_calls = 0
        for call in mock_complete_type.calls[1:]:
            if call.request.method == "POST":
                extract_calls += 1
                assert {"externalId": eid} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls

    def test_complete_template(self, mock_complete_template, mock_status_ok):
        eid = "schematocomplete"
        template = "templatename"
        job = SCAPI.complete(external_id=eid, template_name=template)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"items": []} == job.result
        assert "Completed" == job.status
        assert 123 == job.job_id

        extract_calls = 0
        n_status_calls = 0
        for call in mock_complete_template.calls:
            if call.request.method == "POST":
                extract_calls += 1
                assert {"externalId": eid, "templateName": template} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls

    def test_suggest_instance(self, mock_suggest_instance, mock_suggest_instance_status_ok):
        eid = "schematocomplete"
        template = "templatename"
        job = SCAPI.suggest_instance(external_id=eid, template_name=template)
        assert "Queued" == job.status
        assert {"items": []} == job.result
        extract_calls = 0
        n_status_calls = 0
        for call in mock_suggest_instance.calls:
            if call.request.method == "POST":
                extract_calls += 1
                assert {"externalId": eid, "templateName": template} == jsgz_load(call.request.body)
            else:
                n_status_calls += 1
                assert "/123" in call.request.url
        assert 1 == extract_calls
        assert 1 == n_status_calls
