from typing import Any, Dict, List, Union

from cognite.client._api_client import APIClient

from cognite.experimental.data_classes.geospatial import FeatureType


class ExperimentalGeospatialAPI(APIClient):

    _RESOURCE_PATH = "/spatial/featuretypes"

    def create_feature_type(
        self,
        external_id: str = None,
        created_time: int = None,
        last_updated_time: int = None,
        attributes: Dict[str, Any] = None,
        cognite_client=None,
    ) -> FeatureType:
        """`Creates a feature type`

        Args:

        Returns:
            FeatureType: The created feature type.
        """
        url = self._RESOURCE_PATH
        feature_type_body = {"items": [{"externalId": external_id, "attributes": attributes}]}
        res = self._post(url, json=feature_type_body)
        return FeatureType._load(res.json()["items"][0])

    def delete_feature_type(self, external_id: Union[str, List[str]] = None,) -> None:
        """`Delete one or more feature type`
        """
        self._delete_multiple(external_ids=external_id, wrap_ids=True)
