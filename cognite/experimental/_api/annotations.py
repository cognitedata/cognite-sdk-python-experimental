from typing import Dict, List, Optional, Tuple, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type, to_camel_case, to_snake_case
from cognite.experimental.data_classes import Annotation, AnnotationFilter, AnnotationList


class AnnotationsAPI(APIClient):
    _RESOURCE_PATH = "/context/annotations"
    _LIST_CLASS = AnnotationList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, annotations: List[Annotation]) -> List[Annotation]:

        [assert_type(annotation, "annotation", [Annotation]) for annotation in annotations]
        # response = self._post(
        #     self._RESOURCE_PATH + "/", json={"items": [annotation.dump(camel_case=True) for annotation in annotations]}
        # )
        # return self._response_to_annotations(response)
        return self._create_multiple(items=annotations)

    def list(self, limit: int = None, filter: AnnotationFilter = None):
        assert_type(limit, "limit", [int], allow_none=True)
        assert_type(filter, "filter", [AnnotationFilter], allow_none=True)
        filter = filter.dump(camel_case=True)
        print(filter)
        if filter.get("annotatedResourceIds"):
            filter["annotatedResourceIds"] = [
                {to_camel_case(k): v for k, v in f.items()} for f in filter["annotatedResourceIds"]
            ]

        if limit is None or limit == -1 or limit > self._LIST_LIMIT:
            limit = self._LIST_LIMIT

        response = self._post(self._RESOURCE_PATH + "/list", json={"limit": limit, "filter": filter})
        return self._response_to_annotations(response)

    def delete(self, id: Union[int, List[int]] = None, external_id: Union[str, List[str]] = None) -> None:
        self._delete_multiple(ids=id, external_ids=external_id, wrap_ids=True)

    @staticmethod
    def _response_to_annotations(response):
        items = response.json()["items"]
        snake_cased_items = [{to_snake_case(k): v for k, v in item.items()} for item in items]

        return [Annotation(**item) for item in snake_cased_items]
