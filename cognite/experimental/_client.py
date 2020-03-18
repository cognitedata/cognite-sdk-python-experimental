import os

from cognite.client._api.datapoints import DatapointsAPI
from cognite.client._cognite_client import CogniteClient as Client
from cognite.experimental._api.assets import ExperimentalAssetsAPI
from cognite.experimental._api.entity_extraction import EntityExtractionAPI
from cognite.experimental._api.entity_matching import EntityMatchingAPI
from cognite.experimental._api.model_hosting import ModelHostingAPI
from cognite.experimental._api.pnid_parsing import PNIDParsingAPI
from cognite.experimental._api.relationships import RelationshipsAPI
from cognite.experimental._api.resource_typing import ResourceTypingAPI
from cognite.experimental._api.synthetic_time_series import SyntheticDatapointsAPI
from cognite.experimental._api.types import TypesAPI


class ExperimentalDatapointsApi(DatapointsAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synthetic = SyntheticDatapointsAPI(self._config, api_version="playground", cognite_client=self)


class CogniteClient(Client):
    """Initializes cognite client, with experimental extensions.

    Args:
        * api_key (str): Your api key. If not given, looks for it in environment variables COGNITE_API_KEY and [PROJECT]_API_KEY
        * server (str): Sets base_url to https://[server].cognitedata.com, e.g. server=greenfield.
        * max_workers_async (int): Maximum number of worker threads for the asynchronous job queue. Defaults to max_workers (10).
        * `**kwargs`: other arguments are passed to the SDK.
    """

    def __init__(self, server=None, *args, **kwargs):
        if "base_url" not in kwargs and server is not None:
            kwargs["base_url"] = "https://" + server + ".cognitedata.com"

        if "client_name" not in kwargs and not os.environ.get("COGNITE_CLIENT_NAME"):
            kwargs["client_name"] = "Cognite Experimental SDK"

        if "api_key" not in kwargs and not os.environ.get("COGNITE_API_KEY") and "project" in kwargs:
            key = kwargs["project"].upper().replace("-", "_") + "_API_KEY"
            if os.environ.get(key):
                kwargs["api_key"] = os.environ[key]
            else:
                raise ValueError(
                    "Did not find api key variable in environment, searched COGNITE_API_KEY and {}".format(key)
                )

        super().__init__(*args, **kwargs)
        self.relationships = RelationshipsAPI(self._config, api_version="playground", cognite_client=self)
        self.datapoints = ExperimentalDatapointsApi(self._config, api_version="v1", cognite_client=self)
        self.model_hosting = ModelHostingAPI(self._config, api_version="playground", cognite_client=self)

        self.assets_playground = ExperimentalAssetsAPI(self._config, api_version="playground", cognite_client=self)
        self.types = TypesAPI(self._config, api_version="playground", cognite_client=self)

        self.entity_matching = EntityMatchingAPI(self._config, api_version="playground", cognite_client=self)
        self.entity_extraction = EntityExtractionAPI(self._config, api_version="playground", cognite_client=self)
        self.pnid_parsing = PNIDParsingAPI(self._config, api_version="playground", cognite_client=self)
        self.resource_typing = ResourceTypingAPI(self._config, api_version="playground", cognite_client=self)
