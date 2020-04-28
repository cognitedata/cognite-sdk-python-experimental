from typing import Dict, List, Tuple, Union

import requests

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.client.data_classes import FileMetadataList
from cognite.experimental.data_classes.unstructured import UnstructuredSearchHighlightList


class GrepAPI(APIClient):
    _GREP_RESOURCE_PATH = "/files/unstructured"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._DPS_LIMIT = 10000

    def search(
        self, query: str, highlight: bool = False, filter: Dict = None, aggregates: Dict = None, limit: int = None,
    ) -> Union[FileMetadataList, Tuple[FileMetadataList, UnstructuredSearchHighlightList]]:
        """Grep stuff"""

        body = {"filter": filter, "search": {"query": query, "highlight": highlight}, "aggregates": aggregates}
        resp = self._post(url_path=self._GREP_RESOURCE_PATH + "/search", json=body)

        items = resp.json()["items"]
        files_res = FileMetadataList._load([item["item"] for item in items], cognite_client=self._cognite_client)
        if highlight:
            highlight_res = UnstructuredSearchHighlightList._load([item["highlight"] for item in items])
            return files_res, highlight_res
        return files_res

    def download(self, id: int = None, external_id: str = None) -> str:
        """Download OCR results"""

        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        resp = self._post(
            url_path=self._GREP_RESOURCE_PATH + "/downloadlink/parsed",
            json={"items": [{"id": id, "externalId": external_id}]},
        )
        download_url = resp.json()["items"][0]["downloadUrl"]
        return requests.get(download_url).text
