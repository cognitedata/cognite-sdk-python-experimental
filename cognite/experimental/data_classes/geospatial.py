from typing import Any, Dict, List

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class RasterMetadata:
    """Raster metadata"""

    def __init__(self, **properties):
        for key in properties:
            setattr(self, key, properties[key])

    @classmethod
    def _load(cls, resource: Dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class MvpMappingsDefinition(CogniteResource):
    """MVT mappings definition"""

    def __init__(
        self, external_id: str = None, mappings: List[Dict[str, Any]] = None, cognite_client=None,
    ):
        self.external_id = external_id
        self.mappings = mappings
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class MvpMappingsDefinitionList(CogniteResourceList):
    _RESOURCE = MvpMappingsDefinition
    _ASSERT_CLASSES = False
