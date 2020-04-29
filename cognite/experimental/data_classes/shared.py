# GenPropertyClass: AssetIdsFilter
from typing import List

from cognite.client.data_classes._base import CognitePropertyClassUtil


# GenPropertyClass: AssetIdsFilter
class AssetIdsFilter(dict):
    """Only include files that reference these specific asset IDs.

    Args:
        contains_all (List[int]): Values for this field must match all values in this array
        contains_any (List[int]): Values for this field must match one of the values in this array
    """

    def __init__(self, contains_all: List[int] = None, contains_any: List[int] = None, **kwargs):
        self.contains_all = contains_all
        self.contains_any = contains_any
        self.update(kwargs)

    contains_all = CognitePropertyClassUtil.declare_property("containsAll")
    contains_any = CognitePropertyClassUtil.declare_property("containsAny")

    # GenStop


class GeoShape(dict):
    def __init__(self, type: str = None, coordinates: List = None, **kwargs):
        self.type = type
        self.coordinates = coordinates
        self.update(kwargs)

    type = CognitePropertyClassUtil.declare_property("type")
    coordinates = CognitePropertyClassUtil.declare_property("coordinates")
