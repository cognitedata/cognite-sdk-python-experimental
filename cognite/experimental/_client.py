import os
from typing import Callable, Dict, List, Optional, Union

from cognite.client import ClientConfig, global_config
from cognite.client._api_client import APIClient
from cognite.client.beta import CogniteClient as Client
from cognite.client.credentials import OAuthClientCredentials

from cognite.experimental._api.alerts import AlertsAPI
from cognite.experimental._api.annotations import AnnotationsAPI
from cognite.experimental._api.document_parsing import DocumentParsingAPI
from cognite.experimental._api.entity_matching import EntityMatchingAPI
from cognite.experimental._api.extractionpipelines import ExperimentalExtractionPipelinesAPI
from cognite.experimental._api.geospatial import ExperimentalGeospatialAPI
from cognite.experimental._api.legacy_annotations import LegacyAnnotationsAPI
from cognite.experimental._api.match_rules import MatchRulesAPI
from cognite.experimental._api.pnid_object_detection import PNIDObjectDetectionAPI
from cognite.experimental._api.pnid_parsing import PNIDParsingAPI
from cognite.experimental._api.templatecompletion import ExperimentalTemplatesAPI

APIClient._RETRYABLE_POST_ENDPOINT_REGEX_PATTERNS |= {
    "^" + path + "(\?.*)?$" for path in ("/(types|labels|templates)/(list|byids|search)",)
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

        self.document_parsing = DocumentParsingAPI(self._config, api_version="playground", cognite_client=self)
        self.entity_matching = EntityMatchingAPI(self._config, api_version="playground", cognite_client=self)
        self.match_rules = MatchRulesAPI(self._config, api_version="playground", cognite_client=self)
        self.pnid_parsing = PNIDParsingAPI(self._config, api_version="playground", cognite_client=self)
        self.pnid_object_detection = PNIDObjectDetectionAPI(self._config, api_version="playground", cognite_client=self)
        self.legacy_annotations = LegacyAnnotationsAPI(self._config, api_version="playground", cognite_client=self)
        self.annotations = AnnotationsAPI(self._config, api_version="playground", cognite_client=self)

        self.extraction_pipelines = ExperimentalExtractionPipelinesAPI(
            self._config, api_version="playground", cognite_client=self
        )

        # template completion only
        self.templates = ExperimentalTemplatesAPI(self._config, api_version=self._API_VERSION, cognite_client=self)
