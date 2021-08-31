import json as _json
from typing import List, Optional, Union

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    TransformationDestination,
    TransformationSchemaColumn,
    TransformationSchemaColumnList,
)


class TransformationSchemaAPI(APIClient):
    _RESOURCE_PATH = "/transformations/schema"
    _LIST_CLASS = TransformationSchemaColumnList

    def retrieve(self, destination: TransformationDestination = None) -> TransformationSchemaColumnList:
        """`Get expected schema for a transformation destination. <https://docs.cognite.com/api/playground/#operation/transformations>`_

        Args:
            destination (TransformationDestination): destination for which the schema is requested.

        Returns:
            TransformationSchemaColumnList: List of column descriptions

        Example:

            Get the schema for a transformation producing assets::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import TransformationDestination
                >>> c = CogniteClient()
                >>> columns = c.transformations.schema.retrieve(destination = TransformationDestination.assets())
        """

        url_path = utils._auxiliary.interpolate_and_url_encode(
            self._RESOURCE_PATH + "/{}", str(destination.schema_type)
        )

        return self._list(method="GET", limit=LIST_LIMIT_CEILING, resource_path=url_path)
