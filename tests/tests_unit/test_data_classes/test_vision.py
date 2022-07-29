import json
from typing import Any, Dict, List, Optional, Type, Union
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from cognite.client import CogniteClient
from cognite.client.data_classes.contextualization import JobStatus
from cognite.client.utils._auxiliary import to_snake_case

from cognite.experimental.data_classes import Annotation, AnnotationFilter, AnnotationUpdate, annotations
from cognite.experimental.data_classes.annotation_types.images import TextRegion
from cognite.experimental.data_classes.annotation_types.primitives import BoundingBox
from cognite.experimental.data_classes.vision import AnnotatedItem, AnnotatedObject, AnnotateJobResults
from cognite.experimental.utils import resource_to_camel_case, resource_to_snake_case

mock_annotations_dict: Dict[str, Any] = {
    "textAnnotations": [
        {"text": "a", "textRegion": {"xMin": 0.1, "xMax": 0.2, "yMin": 0.3, "yMax": 0.4}, "confidence": 0.1}
    ]
}
mock_annotated_object = AnnotatedObject(
    text_annotations=[
        TextRegion(
            text="a",
            text_region=BoundingBox(x_min=0.1, x_max=0.2, y_min=0.3, y_max=0.4),
            confidence=0.1,
        )
    ]
)


class TestAnnotatedObject:
    def test_get_feature_class(self) -> None:
        assert AnnotatedObject._get_feature_class(Optional[List[str]]) == str
        assert AnnotatedObject._get_feature_class(Optional[List[List[str]]]) == List[str]
        assert AnnotatedObject._get_feature_class(Optional[List[float]]) == float
        assert AnnotatedObject._get_feature_class(Optional[List[Union[int, str]]]) == Union[int, str]
        assert AnnotatedObject._get_feature_class(Optional[List[AnnotatedObject]]) == AnnotatedObject
        assert AnnotatedObject._get_feature_class(Optional[List[Dict[str, TextRegion]]]) == Dict[str, TextRegion]


class TestAnnotatedItem:
    def test_process_annotations_dict(self) -> None:
        useless_kwargs = {"foo": 1, "bar": "baz"}  # these should be ignored
        assert (
            AnnotatedItem._process_annotations_dict({**mock_annotations_dict, **useless_kwargs})
            == mock_annotated_object
        )

    @pytest.mark.parametrize(
        "resource, expected_item",
        [
            (
                {"fileId": 1, "fileExternalId": "a", "annotations": None},
                AnnotatedItem(file_id=1, file_external_id="a", annotations=None),
            ),
            (
                {"fileId": 1, "annotations": mock_annotations_dict},
                AnnotatedItem(file_id=1, annotations=mock_annotations_dict),
            ),
        ],
        ids=["valid_annotated_item_no_annotations", "valid_annotated_item"],
    )
    def test_load(self, resource: Dict[str, Any], expected_item: AnnotatedItem) -> None:
        annotated_item = AnnotatedItem._load(resource)
        assert annotated_item == expected_item

    @pytest.mark.parametrize(
        "item, expected_dump, camel_case",
        [
            (
                AnnotatedItem(file_id=1, file_external_id="a", annotations=None),
                {"file_id": 1, "file_external_id": "a"},
                False,
            ),
            (
                AnnotatedItem(file_id=1, file_external_id="a", annotations=mock_annotations_dict),
                {"fileId": 1, "fileExternalId": "a", "annotations": resource_to_camel_case(mock_annotations_dict)},
                True,
            ),
        ],
        ids=["valid_dump_no_annotations", "valid_dump_with_annotation_camel_case"],
    )
    def test_dump(self, item: AnnotatedItem, expected_dump: Dict[str, Any], camel_case: bool) -> None:
        assert item.dump(camel_case) == expected_dump


class TestAnnotateJobResults:
    @patch("cognite.experimental.data_classes.vision.ContextualizationJob.result", new_callable=PropertyMock)
    @pytest.mark.parametrize(
        "status, result, expected_items",
        [
            (JobStatus.QUEUED, None, None),
            (
                JobStatus.COMPLETED,
                {"items": [{"fileId": 1, "annotations": mock_annotations_dict}]},
                [AnnotatedItem(file_id=1, annotations=mock_annotations_dict)],
            ),
        ],
        ids=["non_completed_job", "completed_job"],
    )
    def test_items_property(
        self, mock_result: MagicMock, status: JobStatus, result: Optional[Dict], expected_items: Optional[List]
    ) -> None:
        cognite_client = MagicMock(spec=CogniteClient)
        mock_result.return_value = result
        job = AnnotateJobResults(status=status.value, cognite_client=cognite_client)
        assert job.items == expected_items

    @patch("cognite.experimental.data_classes.vision.ContextualizationJob.result", new_callable=PropertyMock)
    @pytest.mark.parametrize(
        "file_id, expected_item, error_message",
        [
            (1, AnnotatedItem(file_id=1, file_external_id="foo", annotations=mock_annotations_dict), None),
            (1337, None, "File with id 1337 not found in results"),
        ],
        ids=["valid_unique_id", "non_existing_id"],
    )
    def test_get_item(
        self,
        mock_result: MagicMock,
        file_id: int,
        expected_item: Optional[AnnotatedItem],
        error_message: Optional[str],
    ) -> None:
        cognite_client = MagicMock(spec=CogniteClient)
        mock_result.return_value = {
            "items": [
                {
                    "fileId": i + 1,
                    "fileExternalId": "foo",
                    "annotations": mock_annotations_dict,
                }
                for i in range(2)
            ]
        }
        job = AnnotateJobResults(cognite_client=cognite_client)
        if error_message is not None:
            with pytest.raises(IndexError, match=error_message):
                job[file_id]
        else:
            assert job[file_id] == expected_item
