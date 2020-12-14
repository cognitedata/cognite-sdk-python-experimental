from typing import *

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental.data_classes import Integration, IntegrationList, IntegrationUpdate


class IntegrationsAPI(APIClient):
    _RESOURCE_PATH = "/integrations"
    _LIST_CLASS = IntegrationList

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[Integration]:
        """`Retrieve a single Integration by id. `_

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID

        Returns:
            Optional[Integration]: Requested integration or None if it does not exist.

        Examples:

            Get integration by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.integrations.retrieve(id=1)

            Get integration by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.integrations.retrieve(external_id="1")
        """

        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def retrieve_multiple(
        self,
        ids: Optional[List[int]] = None,
        external_ids: Optional[List[str]] = None,
        ignore_unknown_ids: bool = False,
    ) -> IntegrationList:
        """`Retrieve multiple integrations by ids and external ids. <>`_

        Args:
            ids (List[int], optional): IDs
            external_ids (List[str], optional): External IDs
            ignore_unknown_ids (bool): Ignore IDs and external IDs that are not found rather than throw an exception.

        Returns:
            IntegrationList: The requested integrations.

        Examples:

            Get integrations by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.integrations.retrieve_multiple(ids=[1, 2, 3])

            Get assets by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.integrations.retrieve_multiple(external_ids=["abc", "def"], ignore_unknown_ids=True)
        """
        utils._auxiliary.assert_type(ids, "id", [List], allow_none=True)
        utils._auxiliary.assert_type(external_ids, "external_id", [List], allow_none=True)
        return self._retrieve_multiple(
            ids=ids, external_ids=external_ids, ignore_unknown_ids=ignore_unknown_ids, wrap_ids=True
        )

    def list(self, limit: int = 25) -> IntegrationList:
        """`List integrations <>`_

        Args:
            limit (int, optional): Maximum number of integrations to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            IntegrationList: List of requested integrations

        Examples:

            List integrations::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> integration_list = c.integrations.list(limit=5)
        """

        return self._list(method="GET", limit=limit,)

    def create(self, integration: Union[Integration, List[Integration]]) -> Union[Integration, IntegrationList]:
        """`Create one or more integrations. <>`_

        You can create an arbitrary number of integrations, and the SDK will split the request into multiple requests.

        Args:
            integration (Union[Integration, List[Integration]]): Integration or list of integrations to create.

        Returns:
            Union[Integration, IntegrationList]: Created integration(s)

        Examples:

            Create new integrations::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import Integration
                >>> c = CogniteClient()
                >>> integrations = [Integration(name="integration",...), Integration(name="integration2",...)]
                >>> res = c.integrations.create(integrations)
        """
        utils._auxiliary.assert_type(integration, "integration", [Integration, list])
        return self._create_multiple(integration)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None,) -> None:
        """`Delete one or more integrations <>`_

            Args:
                id (Union[int, List[int]): Id or list of ids
                external_id (Union[str, List[str]]): External ID or list of exgernal ids

            Returns:
                None

            Examples:

                Delete integrations by id or external id::

                    >>> from cognite.experimental import CogniteClient
                    >>> c = CogniteClient()
                    >>> c.integrations.delete(id=[1,2,3], external_id="3")
            """
        self._delete_multiple(
            ids=id, external_ids=external_id, wrap_ids=True, extra_body_fields={},
        )

    def update(
        self, item: Union[Integration, IntegrationUpdate, List[Union[Integration, IntegrationUpdate]]]
    ) -> Union[Integration, IntegrationList]:
        """`Update one or more integrations <>`_

        Args:
            item Union[Integration, IntegrationUpdate, List[Union[Integration, IntegratioUpdate]]]): Integration(s) to update

        Returns:
            Union[Integration, IntegrationList]: Updated integration(s)

        Examples:

            Update an integration that you have fetched. This will perform a full update of the integration::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> update = IntegrationUpdate(id=1)
                >>> update.description.set("Another new integration")
                >>> res = c.integrations.update(update)
        """
        return self._update_multiple(items=item)
