from typing import *

from cognite.client import utils
from cognite.client._api_client import APIClient
from cognite.client.data_classes.shared import TimestampRange

from cognite.experimental.data_classes import *


class IntegrationsRunsAPI(APIClient):
    _RESOURCE_PATH = "/integrations/runs"
    _LIST_CLASS = IntegrationRunList

    def list(self, external_id: str, limit: int = 25) -> IntegrationRunList:
        """`List of runs for integration with given external_id <>`_

        Args:
            external_id (str): Integration external Id.
            limit (int, optional): Maximum number of integrations to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            IntegrationRunList: List of requested integration runs

        Examples:

            List integrationRuns::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> runsList = c.integration_runs.list(external_id="test ext id", limit=5)
        """

        return self._list(method="GET", limit=limit, filter={"externalId": external_id})

    def filter(
        self,
        external_id: str,
        status: str = None,
        message_substring: str = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        limit: int = 25,
    ) -> IntegrationRunList:
        """`List of runs for integration with given external_id <>`_

        Args:
            external_id (str): Integration external Id.
            status (str): success/failure/seen.
            message_substring (str): failure message part.
            created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
            limit (int, optional): Maximum number of integrations to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            IntegrationRunList: List of requested integration runs

        Examples:

            Filter integrationRuns::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> runsList = c.integration_runs.filter(external_id="test ext id", status="seen", statuslimit=5)
        """

        filter = IntegrationRunFilter(
            external_id=external_id,
            status=status,
            message=StringFilter(substring=message_substring),
            created_time=created_time,
        ).dump(camel_case=True)
        return self._list(method="POST", limit=limit, filter=filter)

    def create(self, run: Union[IntegrationRun, List[IntegrationRun]]) -> Union[IntegrationRun, IntegrationRunList]:
        """`Create one or more integrationRuns. <>`_

        You can create an arbitrary number of integrationRuns, and the SDK will split the request into multiple requests.

        Args:
            run (Union[IntegrationRun, List[IntegrationRun]]): IntegrationRun or list of integrationRuns to create.

        Returns:
            Union[IntegrationRun, IntegrationRunList]: Created integrationRun(s)

        Examples:

            Create new integrationRuns::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import IntegrationRun
                >>> c = CogniteClient()
                >>> integrationRuns = [IntegrationRun(status="success", external_id="extId"),...]
                >>> res = c.integration_runs.create(integrationRuns)
        """
        utils._auxiliary.assert_type(run, "run", [IntegrationRun, list])
        return self._create_multiple(run)
