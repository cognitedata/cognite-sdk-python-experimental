import os
from typing import Optional

from cognite.client import ClientConfig, global_config
from cognite.client._api_client import APIClient
from cognite.client.beta import CogniteClient as Client
from cognite.client.credentials import OAuthClientCredentials
from cognite.experimental._api.alerts import AlertsAPI
from cognite.experimental._api.extractionpipelines import ExperimentalExtractionPipelinesAPI
from cognite.experimental._api.geospatial import ExperimentalGeospatialAPI
from cognite.experimental._api.hosted_extractors import HostedExtractorsAPI
from cognite.experimental._api.simulators import SimulatorsAPI

APIClient._RETRYABLE_POST_ENDPOINT_REGEX_PATTERNS |= {
    "^" + path + "(\?.*)?$"
    for path in (
        "/(types|labels|templates)/(list|byids|search)",
        "/alerts/deduplicate",
    )
}


class CogniteClient(Client):
    """Initializes cognite client, with experimental extensions.

    Args:
        config (ClientConfig): The configuration for this client.
    """

    def __init__(self, config: Optional[ClientConfig] = None):
        if (client_config := config or global_config.default_client_config) is None:
            credentials = OAuthClientCredentials(
                token_url=os.environ["COGNITE_TOKEN_URL"],
                client_id=os.environ["COGNITE_CLIENT_ID"],
                client_secret=os.environ["COGNITE_CLIENT_SECRET"],
                scopes=os.environ["COGNITE_TOKEN_SCOPES"].split(","),
            )
            client_config = ClientConfig(
                os.environ["COGNITE_CLIENT_NAME"],
                os.environ["COGNITE_PROJECT"],
                credentials,
                base_url=os.environ["COGNITE_BASE_URL"],
            )
        self._config = client_config
        super().__init__(self._config)
        self.geospatial = ExperimentalGeospatialAPI(self._config, api_version="v1", cognite_client=self)
        self.alerts = AlertsAPI(self._config, api_version="v1", cognite_client=self)
        self.simulators = SimulatorsAPI(self._config, api_version="v1", cognite_client=self)

        self.extraction_pipelines = ExperimentalExtractionPipelinesAPI(
            self._config, api_version="playground", cognite_client=self
        )
        self.hosted_extractors = HostedExtractorsAPI(self._config, api_version=self._API_VERSION, cognite_client=self)
