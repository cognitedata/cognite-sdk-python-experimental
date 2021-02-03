import os
from typing import Callable, Dict, List, Optional, Union

from cognite.client._api.datapoints import DatapointsAPI
from cognite.client._api.files import FilesAPI
from cognite.client._api_client import APIClient
from cognite.client.beta import CogniteClient as Client

from cognite.experimental._api.annotations import AnnotationsAPI
from cognite.experimental._api.assets import ExperimentalAssetsAPI
from cognite.experimental._api.document_parsing import DocumentParsingAPI
from cognite.experimental._api.entity_matching import EntityMatchingAPI
from cognite.experimental._api.functions import FunctionsAPI
from cognite.experimental._api.integrationruns import IntegrationsRunsAPI
from cognite.experimental._api.integrations import IntegrationsAPI
from cognite.experimental._api.match_rules import MatchRulesAPI
from cognite.experimental._api.model_hosting import ModelHostingAPI
from cognite.experimental._api.plot_extraction import PlotDataExtractionAPI
from cognite.experimental._api.pnid_object_detection import PNIDObjectDetectionAPI
from cognite.experimental._api.pnid_parsing import PNIDParsingAPI
from cognite.experimental._api.schema_completion import SchemaCompletionAPI
from cognite.experimental._api.templates import TemplatesAPI
from cognite.experimental._api.types import TypesAPI
from cognite.experimental._api.unstructured import GrepAPI


class ExperimentalFilesApi(FilesAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unstructured = GrepAPI(self._config, api_version="playground", cognite_client=self)


APIClient.RETRYABLE_POST_ENDPOINTS |= {
    "/files/unstructured/search",
    "/files/unstructured/downloadlink/parsed",
}
APIClient.RETRYABLE_POST_ENDPOINTS |= {
    f"/{api}/{endpoint}"
    for api in ["types", "labels", "functions", "templates"]
    for endpoint in ["list", "byids", "search"]
}


class CogniteClient(Client):
    """Initializes cognite client, with experimental extensions.

    Args:
        * api_key (str): Your api key. If not given, looks for it in environment variables COGNITE_API_KEY and [PROJECT]_API_KEY
        * server (str): Sets base_url to https://[server].cognitedata.com, e.g. server=greenfield.
        * Other keyword arguments are passed to the base SDK directly.
    """

    def __init__(
        self,
        api_key: str = None,
        project: str = None,
        client_name: str = None,
        base_url: str = None,
        max_workers: int = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        token: Union[str, Callable[[], str], None] = None,
        token_url: Optional[str] = None,
        token_client_id: Optional[str] = None,
        token_client_secret: Optional[str] = None,
        token_scopes: Optional[List[str]] = None,
        token_custom_args: Optional[Dict[str, str]] = None,
        disable_pypi_version_check: Optional[bool] = None,
        debug: bool = False,
        server=None,
        **kwargs,
    ):
        if base_url is None and server is not None:
            base_url = "https://" + server + ".cognitedata.com"

        if client_name is None and not os.environ.get("COGNITE_CLIENT_NAME"):
            client_name = "Cognite Experimental SDK"

        no_auth_args = token is None and token_url is None and api_key is None
        if no_auth_args and not os.environ.get("COGNITE_API_KEY") and project is not None:
            key = project.upper().replace("-", "_") + "_API_KEY"
            if os.environ.get(key):
                api_key = os.environ[key]
            else:
                raise ValueError(
                    "Did not find api key variable in environment, searched COGNITE_API_KEY and {}".format(key)
                )

        super().__init__(
            api_key=api_key,
            project=project,
            client_name=client_name,
            base_url=base_url,
            max_workers=max_workers,
            headers=headers,
            timeout=timeout,
            token=token,
            token_url=token_url,
            token_client_id=token_client_id,
            token_client_secret=token_client_secret,
            token_scopes=token_scopes,
            token_custom_args=token_custom_args,
            disable_pypi_version_check=disable_pypi_version_check,
            debug=debug,
            **kwargs,
        )
        # NEW assets features - e.g. types
        self.assets_playground = ExperimentalAssetsAPI(self._config, api_version="playground", cognite_client=self)

        self.files = ExperimentalFilesApi(self._config, api_version="v1", cognite_client=self)
        self.model_hosting = ModelHostingAPI(self._config, api_version="playground", cognite_client=self)
        self.types = TypesAPI(self._config, api_version="playground", cognite_client=self)

        self.document_parsing = DocumentParsingAPI(self._config, api_version="playground", cognite_client=self)
        self.entity_matching = EntityMatchingAPI(self._config, api_version="playground", cognite_client=self)
        self.match_rules = MatchRulesAPI(self._config, api_version="playground", cognite_client=self)
        self.pnid_parsing = PNIDParsingAPI(self._config, api_version="playground", cognite_client=self)
        self.schemas = SchemaCompletionAPI(self._config, api_version="playground", cognite_client=self)
        self.pnid_object_detection = PNIDObjectDetectionAPI(self._config, api_version="playground", cognite_client=self)
        self.annotations = AnnotationsAPI(self._config, api_version="playground", cognite_client=self)
        self.plot_extraction = PlotDataExtractionAPI(self._config, api_version="playground", cognite_client=self)

        self.functions = FunctionsAPI(self.config, api_version="playground", cognite_client=self)
        self.integrations = IntegrationsAPI(self._config, api_version="playground", cognite_client=self)
        self.integration_runs = IntegrationsRunsAPI(self._config, api_version="playground", cognite_client=self)
        self.templates = TemplatesAPI(self._config, api_version=self._API_VERSION, cognite_client=self)
