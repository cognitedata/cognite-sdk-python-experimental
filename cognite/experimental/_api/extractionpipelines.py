from typing import *

from cognite.client import utils
from cognite.client._api_client import APIClient

from cognite.experimental.data_classes import ExtractionPipeline, ExtractionPipelineList, ExtractionPipelineUpdate


class ExtractionPipelinesAPI(APIClient):
    _RESOURCE_PATH = "/extpipes"
    _LIST_CLASS = ExtractionPipelineList

    def retrieve(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Optional[ExtractionPipeline]:
        """`Retrieve a single ExtractionPipeline by id. `_

        Args:
            id (int, optional): ID
            external_id (str, optional): External ID

        Returns:
            Optional[ExtractionPipeline]: Requested ExtractionPipeline or None if it does not exist.

        Examples:

            Get ExtractionPipeline by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.extraction_pipelines.retrieve(id=1)

            Get ExtractionPipeline by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.extraction_pipelines.retrieve(external_id="1")
        """

        utils._auxiliary.assert_exactly_one_of_id_or_external_id(id, external_id)
        return self._retrieve_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    def retrieve_multiple(
        self,
        ids: Optional[List[int]] = None,
        external_ids: Optional[List[str]] = None,
        ignore_unknown_ids: bool = False,
    ) -> ExtractionPipelineList:
        """`Retrieve multiple ExtractionPipelines by ids and external ids. <>`_

        Args:
            ids (List[int], optional): IDs
            external_ids (List[str], optional): External IDs
            ignore_unknown_ids (bool): Ignore IDs and external IDs that are not found rather than throw an exception.

        Returns:
            ExtractionPipelineList: The requested ExtractionPipelines.

        Examples:

            Get ExtractionPipelines by id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.extraction_pipelines.retrieve_multiple(ids=[1, 2, 3])

            Get assets by external id::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> res = c.extraction_pipelines.retrieve_multiple(external_ids=["abc", "def"], ignore_unknown_ids=True)
        """
        utils._auxiliary.assert_type(ids, "id", [List], allow_none=True)
        utils._auxiliary.assert_type(external_ids, "external_id", [List], allow_none=True)
        return self._retrieve_multiple(
            ids=ids, external_ids=external_ids, ignore_unknown_ids=ignore_unknown_ids, wrap_ids=True
        )

    def list(self, limit: int = 25) -> ExtractionPipelineList:
        """`List ExtractionPipelines <>`_

        Args:
            limit (int, optional): Maximum number of ExtractionPipelines to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            ExtractionPipelineList: List of requested ExtractionPipelines

        Examples:

            List ExtractionPipelines::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> ep_list = c.extraction_pipelines.list(limit=5)
        """

        return self._list(method="GET", limit=limit,)

    def create(
        self, extractionPipeline: Union[ExtractionPipeline, List[ExtractionPipeline]]
    ) -> Union[ExtractionPipeline, ExtractionPipelineList]:
        """`Create one or more ExtractionPipelines. <>`_

        You can create an arbitrary number of ExtractionPipelines, and the SDK will split the request into multiple requests.

        Args:
            extractionPipeline (Union[ExtractionPipeline, List[ExtractionPipeline]]): ExtractionPipeline or list of ExtractionPipelines to create.

        Returns:
            Union[ExtractionPipeline, ExtractionPipelineList]: Created ExtractionPipeline(s)

        Examples:

            Create new ExtractionPipelines::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes import ExtractionPipeline
                >>> c = CogniteClient()
                >>> extpipes = [ExtractionPipeline(name="extPipe1",...), ExtractionPipeline(name="extPipe2",...)]
                >>> res = c.extraction_pipelines.create(extpipes)
        """
        utils._auxiliary.assert_type(extractionPipeline, "extraction_pipeline", [ExtractionPipeline, list])
        return self._create_multiple(extractionPipeline)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None,) -> None:
        """`Delete one or more ExtractionPipelines <>`_

            Args:
                id (Union[int, List[int]): Id or list of ids
                external_id (Union[str, List[str]]): External ID or list of exgernal ids

            Returns:
                None

            Examples:

                Delete ExtractionPipelines by id or external id::

                    >>> from cognite.experimental import CogniteClient
                    >>> c = CogniteClient()
                    >>> c.extraction_pipelines.delete(id=[1,2,3], external_id="3")
            """
        self._delete_multiple(
            ids=id, external_ids=external_id, wrap_ids=True, extra_body_fields={},
        )

    def update(
        self,
        item: Union[
            ExtractionPipeline, ExtractionPipelineUpdate, List[Union[ExtractionPipeline, ExtractionPipelineUpdate]]
        ],
    ) -> Union[ExtractionPipeline, ExtractionPipelineList]:
        """`Update one or more ExtractionPipelines <>`_

        Args:
            item Union[ExtractionPipeline, ExtractionPipelineUpdate, List[Union[ExtractionPipeline, ExtractionPipelineUpdate]]]): ExtractionPipeline(s) to update

        Returns:
            Union[ExtractionPipeline, ExtractionPipelineList]: Updated ExtractionPipeline(s)

        Examples:

            Update an ExtractionPipeline that you have fetched. This will perform a full update of the ExtractionPipeline::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> update = ExtractionPipelineUpdate(id=1)
                >>> update.description.set("Another new extpipe")
                >>> res = c.extraction_pipelines.update(update)
        """
        return self._update_multiple(items=item)
