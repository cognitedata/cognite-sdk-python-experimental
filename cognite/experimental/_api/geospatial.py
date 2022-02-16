import functools
import json
import types
from typing import Any, Dict, Generator

from cognite.client._api.geospatial import GeospatialAPI
from cognite.client.data_classes.geospatial import Feature
from cognite.client.exceptions import CogniteConnectionError
from requests.exceptions import ChunkedEncodingError

from cognite.experimental.data_classes.geospatial import RasterMetadata


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

    _cognite_domain = None

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
        raster_id: str,
        raster_format: str,
        raster_srid: int,
        file: str,
    ) -> RasterMetadata:
        """`Put raster`
        <https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/putRaster>

        Args:
            feature_type_external_id : Feature type definition for the features to create.
            feature_external_id: one feature or a list of features to create
            raster_id: the raster id
            raster_format: the raster input format
            raster_srid: the associated SRID for the raster
            file: the path to the file of the raster

        Returns:
            RasterMetadata: the raster metadata if it was ingested succesfully

        Examples:

            Put a raster in a feature raster attribute:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> feature_type = ...
                >>> feature = ...
                >>> rasterId = ...
                >>> metadata = c.geospatial.put_raster(feature_type, feature, rasterId, "XYZ", 3857, file)
        """
        url_path = (
            self._feature_resource_path(feature_type_external_id)
            + f"/{feature_external_id}/rasters/{raster_id}?format={raster_format}&srid={raster_srid}"
        )

        res = self._do_request(
            "PUT",
            url_path,
            data=open(file, "rb").read(),
            headers={"Content-Type": "application/binary"},
            timeout=self._config.timeout,
        )

        return RasterMetadata._load(res.json(), cognite_client=self._cognite_client)
