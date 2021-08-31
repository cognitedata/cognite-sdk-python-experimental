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
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/createFeatureTypes>

        Args:
            FeatureType (Union[FeatureType, List[FeatureType]]): feature type definition or list of feature type definitions to create.

        Returns:
            Union[FeatureType, FeatureTypeList]: Created feature type definition(s)

        Examples:

            Create new type definitions::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.geospatial import FeatureType
                >>> c = CogniteClient()
                >>> feature_types = [
                ...     FeatureType(external_id="wells", attributes={"location": {"type": "POINT", "srid": 4326}})
                ...     FeatureType(external_id="pipelines", attributes={"location": {"type": "LINESTRING", "srid": 2001}})
                ... ]
                >>> res = c.geospatial.create_feature_types(feature_types)


        Args:

        Returns:
            FeatureType: The created feature types.
        """
        return self._create_multiple(items=feature_type)

    def delete_feature_types(self, external_id: Union[str, List[str]] = None) -> None:
        """`Delete one or more feature type`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/deleteFeatureTypes>

        Args:
            external_id (Union[str, List[str]]): External ID or list of external ids

        Returns:
            None

        Examples:

            Delete feature type definitions external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> c.geospatial.delete_feature_types(external_id=["wells", "pipelines"])
        """
        self._delete_multiple(external_ids=external_id, wrap_ids=True)

    def list_feature_types(self) -> FeatureTypeList:
        """`List feature types`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/listFeatureTypes>

        Returns:
            FeatureTypeList: List of feature types

        Examples:

            Iterate over feature type definitions::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> for feature_type in c.geospatial.list_feature_types():
                ...     feature_type # do something with the feature type definition
        """
        return self._list(method="POST")

    def retrieve_feature_types(self, external_id: Union[str, List[str]] = None) -> FeatureTypeList:
        """`Retrieve feature types`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/getFeatureTypesByIds>

        Args:
            external_id (str, optional): External ID

        Returns:
            FeatureTypeList: Requested Type or None if it does not exist.

        Examples:

            Get Type by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.retrieve_feature_types(external_id="1")
        """
        return self._retrieve_multiple(wrap_ids=True, external_ids=external_id)
