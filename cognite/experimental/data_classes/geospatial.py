from typing import Dict

from cognite.client import utils


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
