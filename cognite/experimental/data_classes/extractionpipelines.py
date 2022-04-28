from typing import Dict, Union

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class ExtractionPipelineConfigRevision(CogniteResource):
    def __init__(
        self,
        external_id: str = None,
        revision: int = None,
        description: str = None,
        created_time: int = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.revision = revision
        self.description = description
        self.created_time = created_time
        self.cognite_client = cognite_client


class ExtractionPipelineConfig(ExtractionPipelineConfigRevision):
    def __init__(
        self,
        external_id: str = None,
        config: str = None,
        revision: int = None,
        description: str = None,
        created_time: int = None,
        cognite_client=None,
    ):
        super(ExtractionPipelineConfig, self).__init__(
            external_id=external_id,
            revision=revision,
            description=description,
            created_time=created_time,
            cognite_client=cognite_client,
        )
        self.config = config


class ExtractionPipelineConfigRevisionList(CogniteResourceList):
    _RESOURCE = ExtractionPipelineConfigRevision
    _ASSERT_CLASSES = False
