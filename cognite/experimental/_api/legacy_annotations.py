from typing import Dict, List, Optional, Tuple, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type, to_camel_case, to_snake_case
from cognite.client.utils._identifier import Identifier, IdentifierSequence

from cognite.experimental.data_classes import (
    LegacyAnnotation,
    LegacyAnnotationFilter,
    LegacyAnnotationList,
    LegacyAnnotationUpdate,
)


class LegacyAnnotationsAPI(APIClient):
    _RESOURCE_PATH = "/context/annotations"
    _LIST_CLASS = LegacyAnnotationList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, annotations: Union[LegacyAnnotation, List[LegacyAnnotation]]) -> LegacyAnnotationList:
        """Create annotations

        Args:
            annotations (Union[Annotation, List[Annotation]]): annotations to create

        Returns:
            AnnotationList: created annotations
        """
        assert_type(annotations, "annotation", [LegacyAnnotation, list])
        return self._create_multiple(
            resource_path=self._RESOURCE_PATH,
            items=annotations,
            list_cls=LegacyAnnotationList,
            resource_cls=LegacyAnnotation,
        )

    def list(self, filter: Union[LegacyAnnotationFilter, Dict], limit: int = 100) -> LegacyAnnotationList:
        """List annotations.

        Args:
            limit (int): Maximum number of annotations to return. Defaults to 100.
            filter (AnnotationFilter, optional): Return annotations with parameter values that matches what is specified. Note that annotated_resource_type is always required.

        Returns:
            AnnotationList: list of annotations
        """
        assert_type(limit, "limit", [int], allow_none=False)
        assert_type(filter, "filter", [LegacyAnnotationFilter, dict], allow_none=False)

        if isinstance(filter, LegacyAnnotationFilter):
            filter = filter.dump(camel_case=True)

        elif isinstance(filter, dict):
            filter = {to_camel_case(k): v for k, v in filter.items()}

        if filter.get("annotatedResourceIds"):
            filter["annotatedResourceIds"] = [
                {to_camel_case(k): v for k, v in f.items()} for f in filter["annotatedResourceIds"]
            ]

        return self._list(
            method="POST", limit=limit, filter=filter, list_cls=LegacyAnnotationList, resource_cls=LegacyAnnotation
        )

    def update(
        self,
        item: Union[LegacyAnnotation, LegacyAnnotationUpdate, List[Union[LegacyAnnotation, LegacyAnnotationUpdate]]],
    ) -> Union[LegacyAnnotation, LegacyAnnotationList]:
        """Update annotations

        Args:
            id (Union[int, List[int]]): ID or list of IDs to be deleted
        """
        return self._update_multiple(
            items=item, list_cls=LegacyAnnotationList, resource_cls=LegacyAnnotation, update_cls=LegacyAnnotationUpdate
        )

    def delete(self, id: Union[int, List[int]]) -> None:
        """Delete annotations

        Args:
            id (Union[int, List[int]]): ID or list of IDs to be deleted
        """
        self._delete_multiple(identifiers=IdentifierSequence.load(ids=id), wrap_ids=True)

    def retrieve_multiple(self, ids: List[int]) -> LegacyAnnotationList:
        """Retrieve annotations by IDs

        Args:
            ids (List[int]]: list of IDs to be retrieved

        Returns:
            AnnotationList: list of annotations
        """
        assert_type(ids, "ids", [List], allow_none=False)
        return self._retrieve_multiple(
            identifiers=IdentifierSequence.load(ids=ids), list_cls=LegacyAnnotationList, resource_cls=LegacyAnnotation
        )

    def retrieve(self, id: int) -> LegacyAnnotation:
        """Retrieve an annotation by id

        Args:
            id (int): id of the annotation to be retrieved

        Returns:
            Annotation: annotation requested
        """
        assert_type(id, "id", [int], allow_none=False)
        return self._retrieve_multiple(
            identifiers=IdentifierSequence.load(ids=id).as_singleton(),
            resource_cls=LegacyAnnotation,
            list_cls=LegacyAnnotationList,
        )
