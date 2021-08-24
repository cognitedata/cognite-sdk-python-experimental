from typing import List, Optional, Union

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental._constants import HANDLER_FILE_NAME, LIST_LIMIT_CEILING, LIST_LIMIT_DEFAULT, MAX_RETRIES
from cognite.experimental.data_classes import (
    OidcCredentials,
    Transformation,
    TransformationDestination,
    TransformationJob,
    TransformationJobBlockade,
    TransformationJobList,
    TransformationList,
)


class TransformationJobsAPI(APIClient):
    _RESOURCE_PATH = "/transformations/jobs"
    _LIST_CLASS = TransformationJobList

    def list(self, limit: Optional[int] = LIST_LIMIT_DEFAULT,) -> TransformationJobList:
        """`List all running transformation jobs. <https://docs.cognite.com/api/playground/#operation/transformationJobs>`_

        Args:
            cursor (str): Cursor for paging through results.
            limit (int): Limits the number of results to be returned. To retrieve all results use limit=-1, default limit is 25.

        Returns:
            TransformationJobList: List of transformation jobs

        Example:

            List transformation jobs::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> transformation_jobs_list = c.transformations.jobs.list()
        """
        if limit in [float("inf"), -1, None]:
            limit = LIST_LIMIT_CEILING

        return self._list(method="GET", limit=limit,)

    def retrieve(self, id: int) -> Optional[TransformationJob]:
        """`Retrieve a single transformation job by id. <https://docs.cognite.com/api/playground/#operation/getTransformationJob>`_

        Args:
            id (int): Job internal Id

        Returns:
            Optional[TransformationJob]: Requested transformation job or None if it does not exist.

        Examples:

            Get transformation job by id:

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.transformations.retrieve(id=1)
        """
        return self._retrieve_multiple(ids=id, wrap_ids=False)
