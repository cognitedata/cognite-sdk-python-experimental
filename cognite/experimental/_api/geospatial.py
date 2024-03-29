from __future__ import annotations

import functools
import json
import types
from typing import Any, Generator, Sequence

from requests.exceptions import ChunkedEncodingError

from cognite.client._api.geospatial import GeospatialAPI
from cognite.client.data_classes.geospatial import Feature, FeatureList, FeatureTypeWrite
from cognite.client.exceptions import CogniteConnectionError
from cognite.client.utils._identifier import IdentifierSequence
from cognite.experimental.data_classes.geospatial import (
    ComputedItemList,
    ComputeOrder,
    FeatureType,
    FeatureTypeList,
    GeospatialTask,
    GeospatialTaskList,
    MvpMappingsDefinition,
    MvpMappingsDefinitionList,
)


def _with_cognite_domain(func):
    @functools.wraps(func)
    def wrapper_with_cognite_domain(self, *args, **kwargs):
        if self._cognite_domain is not None:
            self._config.headers.update({self.X_COGNITE_DOMAIN: self._cognite_domain})
        else:
            self._config.headers.pop(self.X_COGNITE_DOMAIN, None)
        res = func(self, *args, **kwargs)
        return res

    return wrapper_with_cognite_domain


class ExperimentalGeospatialAPI(GeospatialAPI):
    X_COGNITE_DOMAIN = "x-cognite-domain"
    _MVT_RESOURCE_PATH = GeospatialAPI._RESOURCE_PATH + "/mvts"

    _cognite_domain = None

    def set_current_cognite_domain(self, cognite_domain: str):
        self._cognite_domain = cognite_domain

    def get_current_cognite_domain(self):
        return self._cognite_domain

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # https://stackoverflow.com/questions/6034662/python-method-overriding-does-signature-matter
        # skip these methods from parent
        skip_methods = [
            "create_feature_types",
            "list_feature_types",
            "retrieve_feature_types",
            "coordinate_reference_systems",
            "stream_features",
            "compute",
        ]
        for attr_name in GeospatialAPI.__dict__:
            if any([method in attr_name for method in skip_methods]):
                continue
            attr = getattr(self, attr_name)
            if isinstance(attr, types.MethodType):
                wrapped = _with_cognite_domain(getattr(GeospatialAPI, attr_name))
                setattr(ExperimentalGeospatialAPI, attr_name, wrapped)

    @_with_cognite_domain
    def create_feature_types(self, feature_type: FeatureType | Sequence[FeatureType]) -> FeatureType | FeatureTypeList:
        """`Creates feature types`
        <https://developer.cognite.com/api#tag/Geospatial/operation/createFeatureTypes>

        Args:
            feature_type (FeatureType | FeatureTypeWrite | Sequence[FeatureType] | Sequence[FeatureTypeWrite]): feature type definition or list of feature type definitions to create.

        Returns:
            FeatureType | FeatureTypeList: Created feature type definition(s)

        Examples:

            Create new type definitions:

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.geospatial import FeatureTypeWrite
                >>> client = CogniteClient()
                >>> feature_types = [
                ...     FeatureTypeWrite(external_id="wells", properties={"location": {"type": "POINT", "srid": 4326}})
                ...     FeatureTypeWrite(
                ...       external_id="cities",
                ...       properties={"name": {"type": "STRING", "size": 10}},
                ...       search_spec={"name_index": {"properties": ["name"]}}
                ...     )
                ... ]
                >>> res = client.geospatial.create_feature_types(feature_types)
        """
        return self._create_multiple(
            list_cls=FeatureTypeList,
            resource_cls=FeatureType,
            items=feature_type,
            resource_path=f"{self._RESOURCE_PATH}/featuretypes",
            input_resource_cls=FeatureTypeWrite,
        )

    @_with_cognite_domain
    def list_feature_types(self) -> FeatureTypeList:
        """`List feature types`
        <https://developer.cognite.com/api#tag/Geospatial/operation/listFeatureTypes>

        Returns:
            FeatureTypeList: List of feature types

        Examples:

            Iterate over feature type definitions:

                >>> from cognite.experimental import CogniteClient
                >>> client = CogniteClient()
                >>> for feature_type in client.geospatial.list_feature_types():
                ...     feature_type # do something with the feature type definition
        """
        return self._list(
            list_cls=FeatureTypeList,
            resource_cls=FeatureType,
            method="POST",
            resource_path=f"{self._RESOURCE_PATH}/featuretypes",
        )

    def retrieve_feature_types(self, external_id: str | list[str]) -> FeatureType | FeatureTypeList:
        """`Retrieve feature types`
        <https://developer.cognite.com/api#tag/Geospatial/operation/getFeatureTypesByIds>

        Args:
            external_id (str | list[str]): External ID

        Returns:
            FeatureType | FeatureTypeList: Requested Type or None if it does not exist.

        Examples:

            Get Type by external id:

                >>> from cognite.experimental import CogniteClient
                >>> client = CogniteClient()
                >>> res = client.geospatial.retrieve_feature_types(external_id="1")
        """
        identifiers = IdentifierSequence.load(ids=None, external_ids=external_id)
        return self._retrieve_multiple(
            list_cls=FeatureTypeList,
            resource_cls=FeatureType,
            identifiers=identifiers.as_singleton() if identifiers.is_singleton() else identifiers,
            resource_path=f"{self._RESOURCE_PATH}/featuretypes",
        )

    @_with_cognite_domain
    def stream_features(
        self,
        feature_type_external_id: str,
        filter: dict[str, Any],
        properties: dict[str, Any] | None = None,
        allow_crs_transformation: bool = False,
    ) -> Generator[Feature, None, None]:
        resource_path = self._feature_resource_path(feature_type_external_id) + "/search-streaming"
        body = {"filter": filter, "output": {"properties": properties, "jsonStreamFormat": "NEW_LINE_DELIMITED"}}
        params = {"allowCrsTransformation": "true"} if allow_crs_transformation else None

        res = self._do_request(
            "POST",
            url_path=resource_path,
            json=body,
            timeout=self._config.timeout,
            stream=True,
            params=params,
            headers={self.X_COGNITE_DOMAIN: self._cognite_domain},
        )

        try:
            for line in res.iter_lines():
                yield Feature._load(json.loads(line))
        except (ChunkedEncodingError, ConnectionError) as e:
            raise CogniteConnectionError(e)

    @_with_cognite_domain
    def create_mvt_mappings_definitions(
        self,
        mappings_definitions: MvpMappingsDefinition | MvpMappingsDefinitionList,
    ) -> MvpMappingsDefinitionList:
        """`Creates MVP mappings`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialCreateMvtMappings>

        Args:
            mappings_definitions: list of MVT mappings definitions

        Returns:
            MvpMappingsDefinitionList: list of created MVT mappings definitions

        Examples:

            Create MVT mappings, assuming the feature types `aggregated_seismic_surveys` and `seismic_surveys`:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> mvp_mappings_def = MvpMappingsDefinition(
                >>>                        external_id="surveys",
                >>>                        mappings_definitions=[
                ...                            {
                ...                                "featureTypeExternalId": "aggregated_seismic_surveys",
                ...                                "levels": [0,1,2,3,4,5],
                ...                                "geometryProperty": "agg_geom",
                ...                                "featureProperties": ["survey_type"]
                ...                            },
                ...                            {
                ...                                "featureTypeExternalId": "seismic_surveys",
                ...                                "levels": [6,7,8,9,10,11,12,13,14,15],
                ...                                "geometryProperty": "geom",
                ...                                "featureProperties": ["survey_type", "sample_rate"]
                ...                            ),
                ...                        ]
                ...                    )
                >>> res = c.geospatial.create_mvt_mappings_definitions(mvp_mappings_def)
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        return self._create_multiple(
            list_cls=MvpMappingsDefinitionList,
            items=mappings_definitions,
            resource_path=resource_path,
            resource_cls=MvpMappingsDefinition,
        )

    @_with_cognite_domain
    def delete_mvt_mappings_definitions(self, external_id: str | list[str] | None = None) -> None:
        """`Deletes MVP mappings definitions`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialDeleteMvtMappings>

        Args:
            external_id (str | List[str]): the mappings external ids

        Returns:
            None

        Examples:

            Deletes MVT mappings definitions:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.delete_mvt_mappings_definitions(external_id="surveys")
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        return self._delete_multiple(
            IdentifierSequence.load(external_ids=external_id), wrap_ids=True, resource_path=resource_path
        )

    @_with_cognite_domain
    def retrieve_mvt_mappings_definitions(
        self, external_id: str | list[str] | None = None
    ) -> MvpMappingsDefinitionList:
        """`Retrieve MVP mappings definitions`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialGetByIdsMvtMappings>

        Args:
            external_id : the mappings external ids
            external_id (str | List[str]): External ID or list of external ids

        Returns:
            MvpMappingsDefinitionList: the requested mappings or None if it does not exist.

        Examples:

            Retrieve one MVT mapping by its external id:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> c.geospatial.retrieve_mvt_mappings_definitions(external_id="surveys")
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        identifiers = IdentifierSequence.load(external_ids=external_id)
        return self._retrieve_multiple(
            identifiers=identifiers.as_singleton() if identifiers.is_singleton() else identifiers,
            resource_path=resource_path,
            list_cls=MvpMappingsDefinitionList,
            resource_cls=MvpMappingsDefinition,
        )

    @_with_cognite_domain
    def list_mvt_mappings_definitions(self) -> MvpMappingsDefinitionList:
        """`List MVP mappings definitions`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialListMvtMappings>

        Returns:
            MvpMappingsDefinitionList: the requested mappings or EmptyList if it does not exist.

        Examples:

            List MVT mappings:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> c.geospatial.list_mvt_mappings_definitions()
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        return self._list(
            method="POST",
            list_cls=MvpMappingsDefinitionList,
            resource_cls=MvpMappingsDefinition,
            resource_path=resource_path,
        )

    @_with_cognite_domain
    def compute(
        self,
        sub_computes: dict[str, Any] | None = None,
        from_feature_type: str | None = None,
        left_joins: Sequence[dict[str, Any]] | None = None,
        filter: dict[str, Any] | None = None,
        group_by: Sequence[dict[str, Any]] | None = None,
        order_by: Sequence[ComputeOrder] | None = None,
        output: dict[str, Any] | None = None,
        into_feature_type: str | None = None,
        binary_output: dict[str, Any] | None = None,
    ) -> bytes | ComputedItemList | None:
        """`Compute something`
        <https://pr-1717.specs.preview.cogniteapp.com/v1.json.html#operation/compute>

        Args:
            sub_computes (Dict[str, Any]): the sub-computed data for the main compute
            from_feature_type (str): the main feature type external id to compute from
            left_joins (Sequence[Dict[str, Any]]): the feature type to left join with
            filter (Dict[str, Any]): the filter for the main feature type
            group_by (List[Dict[str, Any]]): the list of group by expressions
            order_by (List[ComputeOrder]): the list of order by expressions and direction
            output (Dict[str, Any]): the output json spec
            into_feature_type (str): the feature type where to store the result
            binary_output (Dict[str, Any]): the binary output computation to execute

        Returns:
            bytes | List[ComputedItem] | None

        Examples:

            Compute the area and the perimeter of a direct geometry value:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.compute(
                ...     sub_computes={"geom": { "ewkt": "SRID=4326;POLYGON((0 0,0 10,10 10,10 0, 0 0))"}},
                ...     output={
                ...         "geomArea": {"stArea": {"geometry": {"ref": "geom"}}}
                ...         "geomPerimeter": {"stPerimeter": {"geometry": {"ref": "geom"}}}
                ...     },
                >>> )

            Compute the geotiff image of the union of clipped selection of rasters

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.compute(
                ...     from_feature_type="windspeed",
                ...     filter={"equals": {"property": "tag", "value": "SWE"}},
                ...     binary_output={
                ...         "stAsGeotiff": {
                ...             "raster": {
                ...                 "stUnion": {
                ...                     "raster": {
                ...                         "stClip": {
                ...                             "raster": {"property": "rast"},
                ...                             "geometry": {"ewkt": "SRID=4326;POLYGON((17.410 64.966,17.698 64.653,18.016 65.107,17.410 64.966))"}
                ...                         }
                ...                     }
                ...                 }
                ...             }
                ...         }
                ...     }
                >>> )

            Compute the transformed geometry of a direct geometry value

                >>> client.geospatial.compute(
                ...     output={
                ...         "from4326to3857": {
                ...             "stTransform": {
                ...                 "geometry": {"ewkt": "SRID=4326;POINT(2.353295 48.850908)"},
                ...                 "srid": 3857
                ...             }
                ...         }
                ...     }
                ... )

            Compute multiple transformed geometries of a direct "sub_compute" geometry value

                >>> client.geospatial.compute(
                ...     sub_computes={"paris": {"ewkt": "SRID=4326;POINT(2.353295 48.850908)"}},
                ...     output={
                ...         "from4326to3857": {"stTransform": {"geometry": {"ref": "paris"}, "srid": 3857}},
                ...         "from4326to102016": {"stTransform": {"geometry": {"ref": "paris"}, "srid": 102016}},
                ...     }
                ... )

            Compute the sorted aggregation result from a feature type

                >>> client.geospatial.compute(
                ...     from_feature_type="someFeatureType",
                ...     group_by=[
                ...         {"property": "tag"}
                ...         {"property": "week"}
                ...     ],
                ...     order_by=[
                ...         ComputeOrder({"property": "week"}, "ASC"),
                ...         ComputeOrder({"property": "tag"}, "DESC")
                ...     ],
                ...     output={
                ...         "myTag": {"property": "tag"}
                ...         "myWeek": {"property": "week"}
                ...         "myCount": {"count": {"function": {"property": "tag"}}}
                ...     }
                ... )
                :param into_feature_type:
        """
        sub_computes_json = {"subComputes": sub_computes} if sub_computes is not None else {}
        from_feature_type_json = {"fromFeatureType": from_feature_type} if from_feature_type is not None else {}
        left_joins_json = {"leftJoins": left_joins} if left_joins is not None else {}
        filter_json = {"filter": filter} if filter is not None else {}
        group_by_json = {"groupBy": group_by} if group_by is not None else {}
        order_by_json = (
            {"orderBy": [{"expression": it.expression, "order": it.direction} for it in order_by]}
            if order_by is not None
            else {}
        )
        output_json = {"output": output} if output is not None else {}
        binary_output_json = {"binaryOutput": binary_output} if binary_output is not None else {}
        into_feature_type_json = {"intoFeatureType": into_feature_type} if into_feature_type is not None else {}
        res = self._post(
            url_path=GeospatialAPI._RESOURCE_PATH + "/compute",
            json={
                **sub_computes_json,
                **from_feature_type_json,
                **left_joins_json,
                **filter_json,
                **group_by_json,
                **order_by_json,
                **output_json,
                **into_feature_type_json,
                **binary_output_json,
            },
        )
        content_type = res.headers["Content-Type"].split(";")[0]
        if into_feature_type is not None:
            return None
        if content_type == "application/json":
            return ComputedItemList._load(res.json()["items"], cognite_client=self._cognite_client)
        if content_type == "image/tiff":
            return res.content
        raise ValueError(f"unsupported content type ${content_type}")

    def upsert_features(
        self,
        feature_type_external_id: str,
        feature: Feature | Sequence[Feature] | FeatureList,
        allow_crs_transformation: bool = False,
        chunk_size: int | None = None,
    ) -> Feature | FeatureList:
        """`Upsert features`
        <https://pr-1814.specs.preview.cogniteapp.com/v1.json.html#tag/Geospatial/operation/upsertFeatures>

        Args:
            feature_type_external_id: Feature type definition for the features to upsert.
            feature: one feature or a list of features to upsert or a FeatureList object
            allow_crs_transformation: If true, then input geometries will be transformed into the Coordinate Reference
                System defined in the feature type specification. When it is false, then requests with geometries in
                Coordinate Reference System different from the ones defined in the feature type will result in
                CogniteAPIError exception.
            chunk_size: maximum number of items in a single request to the api

        Returns:
            Feature | FeatureList: Upserted features

        Examples:

            Upsert some features:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> feature_types = [
                ...     FeatureType(
                ...         external_id="my_feature_type",
                ...         properties={
                ...             "location": {"type": "POINT", "srid": 4326},
                ...             "temperature": {"type": "DOUBLE"}
                ...         }
                ...     )
                ... ]
                >>> res = c.geospatial.create_feature_types(feature_types)
                >>> res = c.geospatial.upsert_features(
                ...     feature_type_external_id="my_feature_type",
                ...     feature=Feature(
                ...         external_id="my_feature",
                ...         location={"wkt": "POINT(1 1)"},
                ...         temperature=12.4
                ...     )
                ... )
        """
        if chunk_size is not None and (chunk_size < 1 or chunk_size > self._CREATE_LIMIT):
            raise ValueError(f"The chunk_size must be strictly positive and not exceed {self._CREATE_LIMIT}")
        if isinstance(feature, FeatureList):
            feature = list(feature)
        resource_path = self._feature_resource_path(feature_type_external_id) + "/upsert"
        extra_body_fields = {"allowCrsTransformation": "true"} if allow_crs_transformation else {}
        return self._create_multiple(
            list_cls=FeatureList,
            resource_cls=Feature,
            items=feature,
            resource_path=resource_path,
            extra_body_fields=extra_body_fields,
            limit=chunk_size,
        )

    def create_tasks(
        self,
        session_nonce: str,
        task: GeospatialTask | Sequence[GeospatialTask],
    ) -> GeospatialTask | GeospatialTaskList:
        """`Create tasks`
        <https://pr-1916.specs.preview.cogniteapp.com/v1.json.html#tag/Geospatial/operation/createTasks>

        Args:
            session_nonce: the session nonce to be used by the background worker.
            task: the task specification.

        Returns:
            GeospatialTask | Sequence[GeospatialTask]: created tasks

        Examples:

            Get one task:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> tasks = [
                ...     GeospatialTask(
                ...         external_id="my_task",
                ...         task_type="FEATURES_INGESTION"
                ...         task_spec={
                ...             "fileExternalId": "data.csv",
                ...             "intoFeatureType": "my_feature_type",
                ...             "propeties": ["externalId", "tag"],
                ...             "recreateIndex": True
                ...         }
                ...     )
                ... ]
                >>> res = c.geospatial.create_tasks(tasks)
        """
        return self._create_multiple(
            list_cls=GeospatialTaskList,
            resource_cls=GeospatialTask,
            items=task,
            resource_path=f"{GeospatialAPI._RESOURCE_PATH}/tasks",
            extra_body_fields={"sessionNonce": session_nonce},
        )

    def get_tasks(self, external_id: str | list[str]) -> GeospatialTask | GeospatialTaskList:
        """`Retrieve tasks`
        <https://pr-1916.specs.preview.cogniteapp.com/v1.json.html#tag/Geospatial/operation/getTasksByIds>

        Args:
            external_id: the task external id.

        Returns:
            GeospatialTask | Sequence[GeospatialTask]: the retrieved task(s)

        Examples:

            Retrieve one task:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.get_tasks(external_id="my_task")
        """
        identifiers = IdentifierSequence.load(ids=None, external_ids=external_id)
        return self._retrieve_multiple(
            list_cls=GeospatialTaskList,
            resource_cls=GeospatialTask,
            identifiers=identifiers.as_singleton() if identifiers.is_singleton() else identifiers,
            resource_path=f"{GeospatialAPI._RESOURCE_PATH}/tasks",
        )
