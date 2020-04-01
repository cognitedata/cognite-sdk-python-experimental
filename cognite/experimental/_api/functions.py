from typing import Any, Dict, List

from cognite.client._api_client import APIClient
from cognite.experimental.data_classes import FunctionList


class FunctionsAPI(APIClient):
    def list(self) -> FunctionList:
        """List all functions.

        Returns:
            FunctionList: List of functions
        """
        url = "/functions"
        res = self._get(url)
        return FunctionList._load(res.json()["items"])
