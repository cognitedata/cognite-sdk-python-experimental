import functools
import json
import types
import urllib.parse
from typing import Dict, Generator, Optional, Union

from cognite.client._api.geospatial import GeospatialAPI
from cognite.client.data_classes.geospatial import Feature
from cognite.client.exceptions import CogniteConnectionError, CogniteException
from requests.exceptions import ChunkedEncodingError

from cognite.experimental.data_classes.geospatial import *


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

    @staticmethod
    def _raster_resource_path(feature_type_external_id: str, feature_external_id: str, raster_property_name: str):
        encoded_feature_external_id = urllib.parse.quote(feature_external_id, safe="")
        encoded_raster_property_name = urllib.parse.quote(raster_property_name, safe="")
        return (
            ExperimentalGeospatialAPI._feature_resource_path(feature_type_external_id)
            + f"/{encoded_feature_external_id}/rasters/{encoded_raster_property_name}"
        )

    def set_current_cognite_domain(self, cognite_domain: str):
        self._cognite_domain = cognite_domain

    def get_current_cognite_domain(self):
        return self._cognite_domain

    def __init__(self, *args, **kwargs):
        super(ExperimentalGeospatialAPI, self).__init__(*args, **kwargs)

        for attr_name in GeospatialAPI.__dict__:
            attr = getattr(self, attr_name)
            if (
                "coordinate_reference_systems" not in attr_name
                and "stream_features" not in attr_name
                and isinstance(attr, types.MethodType)
            ):
                wrapped = _with_cognite_domain(getattr(GeospatialAPI, attr_name))
                setattr(ExperimentalGeospatialAPI, attr_name, wrapped)

    @_with_cognite_domain
    def stream_features(
        self,
        feature_type_external_id: str,
        filter: Dict[str, Any],
        properties: Dict[str, Any] = None,
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
    def put_raster(
        self,
        feature_type_external_id: str,
        feature_external_id: str,
        raster_property_name: str,
        raster_format: str,
        raster_srid: int,
        file: str,
        allow_crs_transformation: bool = False,
        raster_scale_x: Optional[float] = None,
        raster_scale_y: Optional[float] = None,
    ) -> RasterMetadata:
        """`Put raster`
        <https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/putRaster>

        Args:
            feature_type_external_id : Feature type definition for the features to create.
            feature_external_id: one feature or a list of features to create
            raster_property_name: the raster property name
            raster_format: the raster input format
            raster_srid: the associated SRID for the raster
            file: the path to the file of the raster
            allow_crs_transformation: When the parameter is false, requests with rasters in Coordinate Reference
                System different from the one defined in the feature type will result in bad request response code.
            raster_scale_x: the X component of the pixel width in units of coordinate reference system
            raster_scale_y: the Y component of the pixel height in units of coordinate reference system

        Returns:
            RasterMetadata: the raster metadata if it was ingested succesfully

        Examples:

            Put a raster in a feature raster property:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> feature_type = ...
                >>> feature = ...
                >>> raster_property_name = ...
                >>> metadata = c.geospatial.put_raster(feature_type, feature, raster_property_name, "XYZ", 3857, file)
        """
        query_params = f"format={raster_format}&srid={raster_srid}"
        if allow_crs_transformation:
            query_params += "&allowCrsTransformation=true"
        if raster_scale_x:
            query_params += f"&scaleX={raster_scale_x}"
        if raster_scale_y:
            query_params += f"&scaleY={raster_scale_y}"
        url_path = (
            self._raster_resource_path(feature_type_external_id, feature_external_id, raster_property_name)
            + f"?{query_params}"
        )
        res = self._do_request(
            "PUT",
            url_path,
            data=open(file, "rb").read(),
            headers={"Content-Type": "application/binary"},
            timeout=self._config.timeout,
        )
        return RasterMetadata._load(res.json(), cognite_client=self._cognite_client)

    @_with_cognite_domain
    def delete_raster(
        self,
        feature_type_external_id: str,
        feature_external_id: str,
        raster_property_name: str,
    ) -> None:
        """`Delete raster`
        <https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/deleteRaster>

        Args:
            feature_type_external_id : Feature type definition for the features to create.
            feature_external_id: one feature or a list of features to create
            raster_property_name: the raster property name

        Returns:
            None

        Examples:

            Delete a raster in a feature raster property:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> feature_type = ...
                >>> feature = ...
                >>> raster_property_name = ...
                >>> c.geospatial.delete_raster(feature_type, feature, raster_property_name)
        """
        url_path = (
            self._raster_resource_path(feature_type_external_id, feature_external_id, raster_property_name) + "/delete"
        )
        self._do_request(
            "POST",
            url_path,
            timeout=self._config.timeout,
        )

    @_with_cognite_domain
    def get_raster(
        self,
        feature_type_external_id: str,
        feature_external_id: str,
        raster_property_name: str,
        raster_format: str,
        raster_options: Dict[str, Any] = None,
        raster_srid: Optional[int] = None,
        raster_scale_x: Optional[float] = None,
        raster_scale_y: Optional[float] = None,
        allow_crs_transformation: bool = False,
    ) -> bytes:
        """`Get raster`
        <https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/getRaster>

        Args:
            feature_type_external_id : Feature type definition for the features to create.
            feature_external_id: one feature or a list of features to create
            raster_property_name: the raster property name
            raster_format: the raster output format
            raster_options: GDAL raster creation key-value options
            raster_srid: the SRID for the output raster
            raster_scale_x: the X component of the output pixel width in units of coordinate reference system
            raster_scale_y: the Y component of the output pixel height in units of coordinate reference system
            allow_crs_transformation: When the parameter is false, requests with output rasters in Coordinate Reference
                System different from the one defined in the feature type will result in bad request response code.

        Returns:
            bytes: the raster data

        Examples:

            Get a raster from a feature raster property:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> feature_type = ...
                >>> feature = ...
                >>> raster_property_name = ...
                >>> raster_data = c.geospatial.get_raster(feature_type, feature, raster_property_name,
                >>>                                       "XYZ", {"SIGNIFICANT_DIGITS": "4"})
        """
        url_path = self._raster_resource_path(feature_type_external_id, feature_external_id, raster_property_name)
        res = self._do_request(
            "POST",
            url_path,
            timeout=self._config.timeout,
            json={
                "format": raster_format,
                "options": raster_options,
                "allowCrsTransformation": (True if allow_crs_transformation else None),
                "srid": raster_srid,
                "scaleX": raster_scale_x,
                "scaleY": raster_scale_y,
            },
        )
        return res.content

    @_with_cognite_domain
    def create_mvt_mappings_definitions(
        self,
        mappings_definitions: Union[MvpMappingsDefinition, MvpMappingsDefinitionList],
    ) -> MvpMappingsDefinitionList:
        """`Creates MVP mappings`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialCreateMvtMappings>

        Args:
            mappings_definitions: list of MVT mappings definitions

        Returns:
            Union[List[Dict[str, Any]]]: list of created MVT mappings definitions

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
            items=mappings_definitions, resource_path=resource_path, cls=MvpMappingsDefinitionList
        )

    @_with_cognite_domain
    def delete_mvt_mappings_definitions(self, external_id: Union[str, List[str]] = None) -> None:
        """`Deletes MVP mappings definitions`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialDeleteMvtMappings>

        Args:
            external_id (Union[str, List[str]]): the mappings external ids

        Returns:
            None

        Examples:

            Deletes MVT mappings definitions:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.geospatial.delete_mvt_mappings_definitions(external_id="surveys")
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        return self._delete_multiple(external_ids=external_id, wrap_ids=True, resource_path=resource_path)

    @_with_cognite_domain
    def retrieve_mvt_mappings_definitions(self, external_id: Union[str, List[str]] = None) -> MvpMappingsDefinitionList:
        """`Retrieve MVP mappings definitions`
        <https://pr-1653.specs.preview.cogniteapp.com/v1.json.html#operation/GeospatialGetByIdsMvtMappings>

        Args:
            external_id : the mappings external ids
            external_id (Union[str, List[str]]): External ID or list of external ids

        Returns:
            MvpMappingsDefinitionList: the requested mappings or None if it does not exist.

        Examples:

            Retrieve one MVT mapping by its external id:

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> c.geospatial.retrieve_mvt_mappings_definitions(external_id="surveys")
        """
        resource_path = ExperimentalGeospatialAPI._MVT_RESOURCE_PATH
        return self._retrieve_multiple(
            wrap_ids=True, external_ids=external_id, resource_path=resource_path, cls=MvpMappingsDefinitionList
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
        return self._list(method="POST", cls=MvpMappingsDefinitionList, resource_path=resource_path)

    @_with_cognite_domain
    def compute(
        self,
        sub_computes: Dict[str, Any] = None,
        from_feature_type: str = None,
        filter: Dict[str, Any] = None,
        output: Dict[str, Any] = None,
        binary_output: Dict[str, Any] = None,
    ) -> Union[bytes, ComputedItemList]:
        """`Compute something`
        <https://pr-1717.specs.preview.cogniteapp.com/v1.json.html#operation/compute>

        Args:
            sub_computes (Dict[str, Any]): the sub-computed data for the main compute
            from_feature_type (str): the main feature type external id to compute from
            filter (Dict[str, Any]): the filter for the main feature type
            output (Dict[str, Any]): the output json spec
            binary_output (Dict[str, Any]): the binary output computation to execute

        Returns:
            Union[bytes,List[ComputedItem]]

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
        """
        sub_computes_json = {"subComputes": sub_computes} if sub_computes is not None else {}
        from_feature_type_json = {"fromFeatureType": from_feature_type} if from_feature_type is not None else {}
        filter_json = {"filter": filter} if filter is not None else {}
        output_json = {"output": output} if output is not None else {}
        binary_output_json = {"binaryOutput": binary_output} if binary_output is not None else {}
        res = self._post(
            url_path=GeospatialAPI._RESOURCE_PATH + "/compute",
            json={
                **sub_computes_json,
                **from_feature_type_json,
                **filter_json,
                **output_json,
                **binary_output_json,
            },
        )
        content_type = res.headers["Content-Type"].split(";")[0]
        if content_type == "application/json":
            return ComputedItemList._load(res.json()["items"], cognite_client=self._cognite_client)
        if content_type == "image/tiff":
            return res.content
        raise ValueError(f"unsupported content type ${content_type}")
