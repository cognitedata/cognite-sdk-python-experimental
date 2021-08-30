from typing import Any, Dict

from cognite.client import utils
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class FeatureType(CogniteResource):
    """A representation of a feature type in the geospatial api.
    """

    def __init__(
        self,
        external_id: str = None,
        created_time: int = None,
        last_updated_time: int = None,
        attributes: Dict[str, Any] = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.attributes = attributes
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Dict, cognite_client=None):
        instance = cls(cognite_client=cognite_client)
        for key, value in resource.items():
            snake_case_key = utils._auxiliary.to_snake_case(key)
            setattr(instance, snake_case_key, value)
        return instance


class FeatureTypeList(CogniteResourceList):
    _RESOURCE = FeatureType
    _ASSERT_CLASSES = False
