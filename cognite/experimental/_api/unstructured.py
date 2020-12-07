from typing import Dict, List, Tuple, Union

import requests
from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental.data_classes.unstructured import UnstructuredAggregateList, UnstructuredSearchResultList


class GrepAPI(APIClient):
    _GREP_RESOURCE_PATH = "/files/unstructured"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._DPS_LIMIT = 10000

    def search(
        self, query: str, highlight: bool = False, filter: Dict = None, aggregates: Dict = None, limit: int = None,
    ) -> UnstructuredSearchResultList:
        """Grep stuff"""
        if limit == -1 or limit == float("inf"):
            limit = None
        body = {
            "filter": filter,
            "search": {"query": query, "highlight": highlight},
            "aggregates": aggregates,
            "limit": limit,
        }
        resp = self._post(url_path=self._GREP_RESOURCE_PATH + "/search", json=body)
        data = resp.json()
        items = data["items"]
        search_results = UnstructuredSearchResultList._load(items, cognite_client=self._cognite_client)
        if aggregates:
            search_results.aggregates = UnstructuredAggregateList._load(
                data["aggregates"], cognite_client=self._cognite_client
            )

        return search_results

    def download(self, id: int = None, external_id: str = None) -> str:
        """Download OCR results"""

        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        resp = self._post(
            url_path=self._GREP_RESOURCE_PATH + "/downloadlink/parsed",
            json={"items": [{"id": id, "externalId": external_id}]},
        )
        download_url = resp.json()["items"][0]["downloadUrl"]
        return requests.get(download_url).text
