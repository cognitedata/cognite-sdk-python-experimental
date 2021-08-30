from typing import Any, Dict, List, Union

from cognite.client._api_client import APIClient

from cognite.experimental.data_classes.geospatial import FeatureType, FeatureTypeList


class ExperimentalGeospatialAPI(APIClient):

    _RESOURCE_PATH = "/spatial/featuretypes"
    _LIST_CLASS = FeatureTypeList
    _ASSERT_CLASSES = False

    def create_feature_types(
        self, feature_type: Union[FeatureType, List[FeatureType]]
    ) -> Union[FeatureType, List[FeatureType]]:
        """`Creates feature types`_

        Args:

        Returns:
            FeatureType: The created feature types.
        """
        return self._create_multiple(items=feature_type)

    def delete_feature_types(self, external_id: Union[str, List[str]] = None) -> None:
        """`Delete one or more feature type`_
        """
        self._delete_multiple(external_ids=external_id, wrap_ids=True)

    def list_feature_types(self) -> FeatureTypeList:
        """`List feature types`_
        """
        return self._list(method="POST")
