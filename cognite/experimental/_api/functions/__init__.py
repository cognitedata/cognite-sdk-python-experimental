from cognite.client._api_client import APIClient
from cognite.experimental._api.functions.functions import FunctionsAPI


class FunctionsRootAPI(APIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = FunctionsAPI(*args, **kwargs)
