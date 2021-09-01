from typing import Any, Dict, List, Union

from cognite.client._api_client import APIClient

from cognite.experimental.data_classes.geospatial import Feature, FeatureList, FeatureType, FeatureTypeList


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

            Create new type definitions:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.geospatial import FeatureType
                >>> c = CogniteClient()
                >>> feature_types = [
                ...     FeatureType(external_id="wells", attributes={"location": {"type": "POINT", "srid": 4326}})
                ...     FeatureType(external_id="pipelines", attributes={"location": {"type": "LINESTRING", "srid": 2001}})
                ... ]
                >>> res = c.geospatial.create_feature_types(feature_types)
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

            Delete feature type definitions external id:

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

            Iterate over feature type definitions:

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
            external_id (Union[str, List[str]]): External ID

        Returns:
            FeatureTypeList: Requested Type or None if it does not exist.

        Examples:

            Get Type by external id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.retrieve_feature_types(external_id="1")
        """
        return self._retrieve_multiple(wrap_ids=True, external_ids=external_id)

    def create_features(
        self, feature_type: FeatureType, feature: Union[Feature, List[Feature]]
    ) -> Union[Feature, List[Feature]]:
        """`Creates features`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/createFeatures>

        Args:
            feature_type : Feature type definition for the features to create.
            feature: one feature or a list of features to create

        Returns:
            Union[Feature, FeatureList]: Created features

        Examples:

            Create a new feature:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.geospatial import FeatureType
                >>> c = CogniteClient()
                >>> my_feature_type = c.geospatial.retrieve_feature_types(external_id="my_feature_type")
                >>> res = c.geospatial.create_features(my_feature_types, Feature(external_id="my_feature", temperature=12.4))
        """
        resource_path = self._feature_resource_path(feature_type)
        return self._create_multiple(items=feature, resource_path=resource_path, cls=FeatureList)

    def delete_features(self, feature_type: FeatureType, external_id: Union[str, List[str]] = None) -> None:
        """`Delete one or more feature`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/deleteFeatures>

        Args:
            feature_type : Feature type definition for the features to delete.
            external_id (Union[str, List[str]]): External ID or list of external ids

        Returns:
            None

        Examples:

            Delete feature type definitions external id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> my_feature_type = c.geospatial.retrieve_feature_types(external_id="my_feature_type")
                >>> c.geospatial.delete_feature(my_feature_type, external_id=my_feature)
        """
        resource_path = self._feature_resource_path(feature_type)
        self._delete_multiple(external_ids=external_id, wrap_ids=True, resource_path=resource_path)

    def retrieve_features(self, feature_type: FeatureType, external_id: Union[str, List[str]] = None) -> FeatureList:
        """`Retrieve features`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/getFeaturesByIds>

        Args:
            feature_type : Feature type definition for the features to retrieve.
            external_id (Union[str, List[str]]): External ID or list of external ids

        Returns:
            FeatureList: Requested features or None if it does not exist.

        Examples:

            Retrieve one feature by its external id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> my_feature_type = c.geospatial.retrieve_feature_types(external_id="my_feature_type")
                >>> c.geospatial.retrieve_feature(my_feature_type, external_id="my_feature")
        """
        resource_path = self._feature_resource_path(feature_type)
        return self._retrieve_multiple(
            wrap_ids=True, external_ids=external_id, resource_path=resource_path, cls=FeatureList
        )

    def update_features(self, feature_type: FeatureType, feature: Union[Feature, List[Feature]]) -> FeatureList:
        """`Update features`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/updateFeatures>

        Args:
            feature_type : Feature type definition for the features to update.
            feature (Union[Feature, List[Feature]]): feature or list of features

        Returns:
            FeatureList: Updated features

        Examples:

            Update one feature:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> my_feature_type = c.geospatial.retrieve_feature_types(external_id="my_feature_type")
                >>> my_feature = c.geospatial.create_features(my_feature_type, Feature(external_id="my_feature", temperature=12.4))
                >>> # do some stuff
                >>> my_updated_feature = c.geospatial.update_features(my_feature_type, Feature(external_id="my_feature", temperature=6.237))
        """
        # updates for feature are not following the patch structure from other resources
        # they are more like a replace so an update looks like a feature creation (yeah, borderline ?)
        resource_path = self._feature_resource_path(feature_type) + "/update"
        return self._create_multiple(feature, resource_path=resource_path, cls=FeatureList)

    def search_features(self, feature_type: FeatureType, filter: Dict[str, Any], limit: int = 100) -> FeatureList:
        """`Search for features`_
        <https://pr-1323.specs.preview.cogniteapp.com/v1.json.html#operation/searchFeatures>

        Args:
            feature_type: the feature type to search for
            filter (Dict[str, Any]): the search filter
            limit (int): maximum number of results

        Returns:
            FeatureList: the filtered features

        Examples:

            Search for features:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> my_feature_type = c.geospatial.retrieve_feature_types(external_id="my_feature_type")
                >>> my_feature = c.geospatial.create_features(my_feature_type, Feature(external_id="my_feature", temperature=12.4))
                >>> res = c.geospatial.search_features(my_feature_type, filter={"range": {"attribute": "temperature", "gt": 12.0}})
                >>> for f in res:
                ...     # do something with the features
        """
        resource_path = self._feature_resource_path(feature_type) + "/search"
        cls = FeatureList
        resource_path = resource_path or self._RESOURCE_PATH
        res = self._post(url_path=resource_path, json={"filter": filter, "limit": limit},)
        return cls._load(res.json()["items"], cognite_client=self._cognite_client)

    def _feature_resource_path(self, feature_type: FeatureType):
        return self._RESOURCE_PATH + "/" + feature_type.external_id + "/features"
