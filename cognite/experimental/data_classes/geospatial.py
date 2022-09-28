from typing import Any, Dict, List

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class MvpMappingsDefinition(CogniteResource):
    """MVT mappings definition"""

    def __init__(
        self,
        external_id: str = None,
        mappings: List[Dict[str, Any]] = None,
        cognite_client=None,
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


class ComputedItem(CogniteResource):
    """A representation of a computed item by the geospatial api."""

    def __init__(self, cognite_client=None, **properties):
        for key in properties:
            setattr(self, key, properties[key])
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class ComputedItemList(CogniteResourceList):
    _RESOURCE = ComputedItem
    _ASSERT_CLASSES = False


class ComputeOrder:
    """An order specification with respect to an expression."""

    def __init__(self, expression: Dict[str, Any], direction: str):
        self.expression = expression
        self.direction = direction
