import re

import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ExtractionPipeline, ExtractionPipelineList, ExtractionPipelineUpdate
from tests.utils import jsgz_load

COGNITE_CLIENT = CogniteClient()
TEST_API = COGNITE_CLIENT.extraction_pipelines


@pytest.fixture
def mock_int_response(rsps):
    response_body = {
        "items": [
            {
                "id": 1,
                "externalId": "int-123",
                "name": "test_name",
                "description": "description",
                "createdTime": 1565965333132,
                "lastUpdatedTime": 1565965333132,
                "dataSetId": 1,
                "contacts": [{"name": "test name", "email": "aaa@cognite.com", "sendNotification": True}],
                "metadata": {"step": "22", "version": "1"},
            }
        ]
    }
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path()) + r"/extpipes(?:/byids|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    yield rsps


@pytest.fixture
def mock_int_empty(rsps):
    response_body = {"items": []}
    url_pattern = re.compile(
        re.escape(TEST_API._get_base_url_with_base_path()) + r"/extpipes(?:/byids|/update|/delete|/list|/search|$|\?.+)"
    )
    rsps.assert_all_requests_are_fired = False

    rsps.add(rsps.POST, url_pattern, status=200, json=response_body)
    rsps.add(rsps.GET, url_pattern, status=200, json=response_body)
    yield rsps


class TestExtractionPipelines:
    def test_retrieve_single(self, mock_int_response):
        res = TEST_API.retrieve(id=1)
        assert isinstance(res, ExtractionPipeline)
        assert mock_int_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_retrieve_multiple(self, mock_int_response):
        res = TEST_API.retrieve_multiple(ids=[1])
        assert isinstance(res, ExtractionPipelineList)
        assert mock_int_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_list(self, mock_int_response):
        res = TEST_API.list(external_id_prefix="19")
        assert mock_int_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_create_single(self, mock_int_response):
        res = TEST_API.create(
            ExtractionPipeline(
                external_id="py test id",
                name="py test",
                description="python generated",
                data_set_id=1,
                schedule="",
                contacts=[{"name": "Alex", "email": "Alex@test.no", "sendNotification": True}],
            )
        )
        assert isinstance(res, ExtractionPipeline)
        assert mock_int_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_create_multiple(self, mock_int_response):
        ep1 = ExtractionPipeline(
            external_id="py test id",
            name="py test",
            description="python generated",
            data_set_id=1,
            schedule="",
            contacts=[{"name": "Alex", "email": "Alex@test.no", "sendNotification": True}],
        )

        ep2 = ExtractionPipeline(
            external_id="py test id2",
            name="py test2",
            description="python generated",
            data_set_id=1,
            schedule="",
            contacts=[{"name": "Alex", "email": "Alex@test.no", "sendNotification": True}],
        )

        res = TEST_API.create([ep1, ep2])
        assert isinstance(res, ExtractionPipelineList)
        assert mock_int_response.calls[0].response.json()["items"] == res.dump(camel_case=True)

    def test_delete_single(self, mock_int_response):
        res = TEST_API.delete(external_id="a")
        assert {"items": [{"externalId": "a"}]} == jsgz_load(mock_int_response.calls[0].request.body)
        assert res is None

    def test_delete_single_byid(self, mock_int_response):
        res = TEST_API.delete(id=1)
        assert {"items": [{"id": 1}]} == jsgz_load(mock_int_response.calls[0].request.body)
        assert res is None

    def test_delete_multiple(self, mock_int_response):
        res = TEST_API.delete(external_id=["a", "b"])
        assert {"items": [{"externalId": "a"}, {"externalId": "b"}]} == jsgz_load(
            mock_int_response.calls[0].request.body
        )
        assert res is None

    def test_update_single(self, mock_int_response):
        res = TEST_API.update(
            ExtractionPipeline(
                external_id="py test id",
                name="py test",
                description="python generated",
                data_set_id=1,
                schedule="",
                contacts=[{"name": "Alex", "email": "Alex@test.no", "sendNotification": True}],
            )
        )
        assert isinstance(res, ExtractionPipeline)
        assert mock_int_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)

    def test_update_single_with_update_class(self, mock_int_response):
        up = ExtractionPipelineUpdate(external_id="py test id")
        up.description.set("New description")
        res = TEST_API.update(up)
        assert isinstance(res, ExtractionPipeline)
        assert mock_int_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)
        assert {
            "items": [{"externalId": "py test id", "update": {"description": {"set": "New description"}}}]
        } == jsgz_load(mock_int_response.calls[0].request.body)

    def test_update_raw_tables_with_update_class(self, mock_int_response):
        up = ExtractionPipelineUpdate(external_id="py test id")
        up.raw_tables.add([{"dbName": "db", "tableName": "table"}])
        res = TEST_API.update(up)
        assert isinstance(res, ExtractionPipeline)
        assert mock_int_response.calls[0].response.json()["items"][0] == res.dump(camel_case=True)
        assert {
            "items": [
                {"externalId": "py test id", "update": {"rawTables": {"add": [{"dbName": "db", "tableName": "table"}]}}}
            ]
        } == jsgz_load(mock_int_response.calls[0].request.body)
