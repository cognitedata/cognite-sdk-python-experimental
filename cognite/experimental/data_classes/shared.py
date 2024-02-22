from __future__ import annotations

from cognite.client.data_classes._base import CogniteObject


# GenPropertyClass: AssetIdsFilter
class AssetIdsFilter(CogniteObject):
    """Only include files that reference these specific asset IDs.

    Args:
        contains_all (list[int]): Values for this field must match all values in this array
        contains_any (list[int]): Values for this field must match with at least one of the values in this array
        missing (bool): Value for the field is missing
    """

    def __init__(
        self,
        contains_all: list[int] | None = None,
        contains_any: list[int] | None = None,
        missing: bool | None = None,
        **kwargs,
    ):
        self.contains_all = contains_all
        self.contains_any = contains_any
        self.missing = missing

    # GenStop


class GeoShape(CogniteObject):
    def __init__(self, type: str | None = None, coordinates: list | None = None):
        self.type = type
        self.coordinates = coordinates
