from cognite.client import utils
from cognite.client._api.extractionpipelines import ExtractionPipelinesAPI

from cognite.experimental.data_classes import ExtractionPipelineConfig, ExtractionPipelineConfigRevisionList


class ExperimentalExtractionPipelinesAPI(ExtractionPipelinesAPI):
    def __init__(self, config: utils._client_config.ClientConfig, api_version: str = None, cognite_client=None):
        super(ExperimentalExtractionPipelinesAPI, self).__init__(
            config=config, api_version=api_version, cognite_client=cognite_client
        )

    def get_config(self, external_id: str) -> ExtractionPipelineConfig:
        response = self._get("/extpipes/config", params={"externalId": external_id})
        return ExtractionPipelineConfig._load(response.json(), cognite_client=self._cognite_client)

    def list_config_revisions(self, external_id: str) -> ExtractionPipelineConfigRevisionList:
        response = self._get("/extpipes/config/revisions", params={"externalId": external_id})
        return ExtractionPipelineConfigRevisionList._load(response.json()["items"], cognite_client=self._cognite_client)

    def new_config(self, config: ExtractionPipelineConfig) -> ExtractionPipelineConfig:
        response = self._post("/extpipes/config", json=config.dump(camel_case=True))
        return ExtractionPipelineConfig._load(response.json(), cognite_client=self._cognite_client)
