from typing import *

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.client.data_classes.shared import TimestampRange

from cognite.experimental.data_classes import *


class ExtractionPipelinesRunsAPI(APIClient):
    _RESOURCE_PATH = "/extpipes/runs"
    _LIST_CLASS = ExtractionPipelineRunList

    def list(
        self,
        external_id: str,
        statuses: List[str] = None,
        message_substring: str = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        limit: int = 25,
    ) -> ExtractionPipelineRunList:
        """`List of runs for ExtractionPipeline with given external_id <>`_

        Args:
            external_id (str): ExtractionPipeline external Id.
            statuses (List[str]): success/failure/seen.
            message_substring (str): failure message part.
            created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
            limit (int, optional): Maximum number of ExtractionPipelines to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            ExtractionPipelineRunList: List of requested ExtractionPipeline runs

        Examples:

            List ExtractionPipeline Runs::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> runsList = c.extraction_pipeline_runs.list(external_id="test ext id", limit=5)

            Filter ExtractionPipeline Runs::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> runsList = c.extraction_pipeline_runs.list(external_id="test ext id", statuses=["seen"], statuslimit=5)
        """

        if statuses is not None or message_substring is not None or created_time is not None:
            filter = ExtractionPipelineRunFilter(
                external_id=external_id,
                statuses=statuses,
                message=StringFilter(substring=message_substring),
                created_time=created_time,
            ).dump(camel_case=True)
            return self._list(method="POST", limit=limit, filter=filter)

        return self._list(method="GET", limit=limit, filter={"externalId": external_id})

    def create(
        self, run: Union[ExtractionPipelineRun, List[ExtractionPipelineRun]]
    ) -> Union[ExtractionPipelineRun, ExtractionPipelineRunList]:
        """`Create one or more ExtractionPipeline Runs. <>`_

        You can create an arbitrary number of ExtractionPipeline Runs, and the SDK will split the request into multiple requests.

        Args:
            run (Union[ExtractionPipelineRun, List[ExtractionPipelineRun]]): ExtractionPipelineRun or list of ExtractionPipeline Runs to create.

        Returns:
            Union[ExtractionPipelineRun, ExtractionPipelineRunList]: Created ExtractionPipeline Run(s)

        Examples:

            Create new ExtractionPipeline Runs::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import ExtractionPipelineRun
                >>> c = CogniteClient()
                >>> extPipeRuns = [ExtractionPipelineRun(status="success", external_id="extId"),...]
                >>> res = c.extraction_pipeline_runs.create(extPipeRuns)
        """
        utils._auxiliary.assert_type(run, "run", [ExtractionPipelineRun, list])
        return self._create_multiple(run)
