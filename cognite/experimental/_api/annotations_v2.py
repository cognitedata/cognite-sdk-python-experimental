from typing import Dict, List, Optional, Tuple, Union

from cognite.client._api_client import APIClient
from cognite.client.data_classes._base import CogniteResource
from cognite.client.utils._auxiliary import assert_type, to_camel_case, to_snake_case

from cognite.experimental.data_classes import AnnotationV2, AnnotationV2Filter, AnnotationV2List, AnnotationV2Update


class AnnotationsV2API(APIClient):
    _RESOURCE_PATH = "/annotations"
    _LIST_CLASS = AnnotationV2List

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, annotations: Union[AnnotationV2, List[AnnotationV2]]) -> Union[AnnotationV2, AnnotationV2List]:
        """Create annotations

        Args:
            annotations (Union[AnnotationV2, List[AnnotationV2]]): annotation(s) to create

        Returns:
            Union[AnnotationV2, AnnotationV2List]: created annotation(s)
        """
        assert_type(annotations, "annotations", [AnnotationV2, list])
        return self._create_multiple(resource_path=self._RESOURCE_PATH + "/", items=annotations)

    def list(self, filter: Union[AnnotationV2Filter, Dict], limit: int = 25) -> AnnotationV2List:
        """List annotations.

        Args:
            limit (int): Maximum number of annotations to return. Defaults to 25.
            filter (AnnotationV2Filter, optional): Return annotations with parameter values that matches what is specified. Note that annotated_resource_type and annotated_resource_ids are always required.

        Returns:
            AnnotationV2List: list of annotations
        """
        assert_type(limit, "limit", [int], allow_none=False)
        assert_type(filter, "filter", [AnnotationV2Filter, dict], allow_none=False)

        if isinstance(filter, AnnotationV2Filter):
            filter = filter.dump(camel_case=True)

        elif isinstance(filter, dict):
            filter = {to_camel_case(k): v for k, v in filter.items()}

        if "annotatedResourceIds" in filter:
            filter["annotatedResourceIds"] = [
                {to_camel_case(k): v for k, v in f.items()} for f in filter["annotatedResourceIds"]
            ]

        if "linkedResourceIds" in filter:
            filter["linkedResourceIds"] = [
                {to_camel_case(k): v for k, v in f.items()} for f in filter["linkedResourceIds"]
            ]

        return self._list(method="POST", limit=limit, filter=filter)

    @staticmethod
    def _convert_resource_to_patch_object(resource: CogniteResource, update_attributes: List[str]):
        if not isinstance(resource, AnnotationV2):
            return APIClient._convert_resource_to_patch_object(resource, update_attributes)
        annotation: AnnotationV2 = resource
        annotation_update = AnnotationV2Update(id=annotation.id)
        for attr in update_attributes:
            getattr(annotation_update, attr).set(getattr(annotation, attr))
        return annotation_update.dump()

    def update(
        self, item: Union[AnnotationV2, AnnotationV2Update, List[Union[AnnotationV2, AnnotationV2Update]]]
    ) -> Union[AnnotationV2, AnnotationV2List]:
        """Update annotations

        Args:
            id (Union[int, List[int]]): ID or list of IDs to be deleted
        """
        return self._update_multiple(items=item)

    def delete(self, id: Union[int, List[int]]) -> None:
        """Delete annotations

        Args:
            id (Union[int, List[int]]): ID or list of IDs to be deleted
        """
        self._delete_multiple(ids=id, wrap_ids=True)

    def retrieve_multiple(self, ids: List[int]) -> AnnotationV2List:
        """Retrieve annotations by IDs

        Args:
            ids (List[int]]: list of IDs to be retrieved

        Returns:
            AnnotationV2List: list of annotations
        """
        assert_type(ids, "ids", [List], allow_none=False)
        return self._retrieve_multiple(ids=ids, wrap_ids=True)

    def retrieve(self, id: int) -> AnnotationV2:
        """Retrieve an annotation by id

        Args:
            id (int): id of the annotation to be retrieved

        Returns:
            AnnotationV2: annotation requested
        """
        assert_type(id, "id", [int], allow_none=False)
        return self._retrieve_multiple(ids=id, wrap_ids=True)
