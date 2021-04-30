from typing import Dict, List, Optional, Tuple, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type, to_camel_case, to_snake_case

from cognite.experimental.data_classes import Annotation, AnnotationFilter, AnnotationList, AnnotationUpdate


class AnnotationsAPI(APIClient):
    _RESOURCE_PATH = "/context/annotations"
    _LIST_CLASS = AnnotationList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, annotations: Union[Annotation, List[Annotation]]) -> AnnotationList:
        """Create annotations

        Args:
            annotations (Union[Annotation, List[Annotation]]): annotations to create

        Returns:
            AnnotationList: created annotations
        """
        assert_type(annotations, "annotation", [Annotation, list])
        return self._create_multiple(resource_path=self._RESOURCE_PATH + "/", items=annotations)

    def list(self, filter: Union[AnnotationFilter, Dict], limit: int = 100) -> AnnotationList:
        """List annotations.

        Args:
            limit (int): Maximum number of annotations to return. Defaults to 100.
            filter (AnnotationFilter, optional): Return annotations with parameter values that matches what is specified. Note that annotated_resource_type is always required.

        Returns:
            AnnotationList: list of annotations
        """
        assert_type(limit, "limit", [int], allow_none=False)
        assert_type(filter, "filter", [AnnotationFilter, dict], allow_none=False)

        if isinstance(filter, AnnotationFilter):
            filter = filter.dump(camel_case=True)

        elif isinstance(filter, dict):
            filter = {to_camel_case(k): v for k, v in filter.items()}

        if filter.get("annotatedResourceIds"):
            filter["annotatedResourceIds"] = [
                {to_camel_case(k): v for k, v in f.items()} for f in filter["annotatedResourceIds"]
            ]

        response = self._post(self._RESOURCE_PATH + "/list", json={"limit": limit, "filter": filter})
        return AnnotationList._load(response.json()["items"])

    def update(
        self, item: Union[Annotation, AnnotationUpdate, List[Union[Annotation, AnnotationUpdate]]]
    ) -> Union[Annotation, AnnotationList]:
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

    def retrieve_multiple(self, ids: List[int]) -> AnnotationList:
        """Retrieve annotations by IDs

        Args:
            ids (List[int]]: list of IDs to be retrieved

        Returns:
            AnnotationList: list of annotations
        """
        assert_type(ids, "ids", [List], allow_none=False)
        return self._retrieve_multiple(ids=ids, wrap_ids=True)

    def retrieve(self, id: int) -> Annotation:
        """Retrieve an annotation by id

        Args:
            id (int): id of the annotation to be retrieved

        Returns:
            Annotation: annotation requested
        """
        assert_type(id, "id", [int], allow_none=False)
        return self._retrieve_multiple(ids=id, wrap_ids=True)
