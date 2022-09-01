from enum import Enum

from cognite.client import ClientConfig
from cognite.client._api_client import APIClient
from cognite.client.beta import CogniteClient as Client

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
from cognite.experimental._api.vision import VisionAPI

APIClient.RETRYABLE_POST_ENDPOINTS |= {
    f"/{api}/{endpoint}" for api in ["types", "labels", "templates"] for endpoint in ["list", "byids", "search"]
}


class ApiVersion(str, Enum):
    Playground = "playground"
    V1 = "v1"


class CogniteClient(Client):
    """Initializes cognite client, with experimental extensions.

    Args:
        * config (ClientConfig): The configuration for this client.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config=config)
        self.geospatial = ExperimentalGeospatialAPI(self._config, api_version=ApiVersion.V1, cognite_client=self)
        self.alerts = AlertsAPI(self._config, api_version=ApiVersion.V1, cognite_client=self)

        self.document_parsing = DocumentParsingAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)
        self.entity_matching = EntityMatchingAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)
        self.match_rules = MatchRulesAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)
        self.pnid_parsing = PNIDParsingAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)
        self.pnid_object_detection = PNIDObjectDetectionAPI(
            self._config, api_version=ApiVersion.Playground, cognite_client=self
        )
        self.legacy_annotations = LegacyAnnotationsAPI(
            self._config, api_version=ApiVersion.Playground, cognite_client=self
        )
        self.annotations = AnnotationsAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)

        self.extraction_pipelines = ExperimentalExtractionPipelinesAPI(
            self._config, api_version=ApiVersion.Playground, cognite_client=self
        )

        # template completion only
        self.templates = ExperimentalTemplatesAPI(self._config, api_version=self._API_VERSION, cognite_client=self)
        self.vision = VisionAPI(self._config, api_version=ApiVersion.Playground, cognite_client=self)
