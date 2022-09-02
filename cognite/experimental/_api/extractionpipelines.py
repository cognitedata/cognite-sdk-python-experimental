from typing import Optional

from cognite.client._api.extractionpipelines import ExtractionPipelinesAPI

from cognite.experimental.data_classes import ExtractionPipelineConfig, ExtractionPipelineConfigRevisionList


class ExperimentalExtractionPipelinesAPI(ExtractionPipelinesAPI):
    def get_config(
        self, external_id: str, revision: Optional[int] = None, active_at_time: Optional[int] = None
    ) -> ExtractionPipelineConfig:
        response = self._get(
            "/extpipes/config", params={"externalId": external_id, "activeAtTime": active_at_time, "revision": revision}
        )
        return ExtractionPipelineConfig._load(response.json(), cognite_client=self._cognite_client)

    def list_config_revisions(self, external_id: str) -> ExtractionPipelineConfigRevisionList:
        response = self._get("/extpipes/config/revisions", params={"externalId": external_id})
        return ExtractionPipelineConfigRevisionList._load(response.json()["items"], cognite_client=self._cognite_client)

    def new_config(self, config: ExtractionPipelineConfig) -> ExtractionPipelineConfig:
        response = self._post("/extpipes/config", json=config.dump(camel_case=True))
        return ExtractionPipelineConfig._load(response.json(), cognite_client=self._cognite_client)

    def revert_config(self, external_id: str, revision: int) -> ExtractionPipelineConfig:
        response = self._post("/extpipes/config/revert", json={"externalId": external_id, "revision": revision})
        return ExtractionPipelineConfig._load(response.json(), cognite_client=self._cognite_client)
