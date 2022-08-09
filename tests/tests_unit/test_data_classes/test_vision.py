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
from cognite.experimental.data_classes.vision import VisionExtractItem, VisionExtractJob, VisionExtractPredictions
from cognite.experimental.utils import resource_to_camel_case, resource_to_snake_case

mock_vision_predictions_dict: Dict[str, Any] = {
    "textAnnotations": [  # TODO: rename to predictions
        {"text": "a", "textRegion": {"xMin": 0.1, "xMax": 0.2, "yMin": 0.3, "yMax": 0.4}, "confidence": 0.1}
    ]
}
mock_vision_extract_predictions = VisionExtractPredictions(
    text_annotations=[  # TODO: rename to predictions
        TextRegion(
            text="a",
            text_region=BoundingBox(x_min=0.1, x_max=0.2, y_min=0.3, y_max=0.4),
            confidence=0.1,
        )
    ]
)


class TestVisionExtractPredictions:
    def test_get_feature_class(self) -> None:
        assert VisionExtractPredictions._get_feature_class(Optional[List[str]]) == str
        assert VisionExtractPredictions._get_feature_class(Optional[List[List[str]]]) == List[str]
        assert VisionExtractPredictions._get_feature_class(Optional[List[float]]) == float
        assert VisionExtractPredictions._get_feature_class(Optional[List[Union[int, str]]]) == Union[int, str]
        assert (
            VisionExtractPredictions._get_feature_class(Optional[List[VisionExtractPredictions]])
            == VisionExtractPredictions
        )
        assert (
            VisionExtractPredictions._get_feature_class(Optional[List[Dict[str, TextRegion]]]) == Dict[str, TextRegion]
        )


class TestVisionExtractItem:
    def test_process_predictions_dict(self) -> None:
        useless_kwargs = {"foo": 1, "bar": "baz"}  # these should be ignored
        assert (
            VisionExtractItem._process_predictions_dict({**mock_vision_predictions_dict, **useless_kwargs})
            == mock_vision_extract_predictions
        )

    @pytest.mark.parametrize(
        "resource, expected_item",
        [
            (
                {"fileId": 1, "fileExternalId": "a", "annotations": None},  # TODO: rename to predictions
                VisionExtractItem(file_id=1, file_external_id="a", predictions=None),
            ),
            (
                {"fileId": 1, "annotations": mock_vision_predictions_dict},
                VisionExtractItem(file_id=1, predictions=mock_vision_predictions_dict),
            ),
        ],
        ids=["valid_vision_extract_item_no_predictions", "valid_vision_extract_item"],
    )
    def test_load(self, resource: Dict[str, Any], expected_item: VisionExtractItem) -> None:
        vision_extract_item = VisionExtractItem._load(resource)
        assert vision_extract_item == expected_item

    @pytest.mark.parametrize(
        "item, expected_dump, camel_case",
        [
            (
                VisionExtractItem(file_id=1, file_external_id="a", predictions=None),
                {"file_id": 1, "file_external_id": "a"},
                False,
            ),
            (
                VisionExtractItem(file_id=1, file_external_id="a", predictions=mock_vision_predictions_dict),
                {
                    "fileId": 1,
                    "fileExternalId": "a",
                    "annotations": resource_to_camel_case(mock_vision_predictions_dict),
                },  # TODO: rename to predictions
                True,
            ),
        ],
        ids=["valid_dump_no_predictions", "valid_dump_with_predictions_camel_case"],
    )
    def test_dump(self, item: VisionExtractItem, expected_dump: Dict[str, Any], camel_case: bool) -> None:
        assert item.dump(camel_case) == expected_dump


class TestVisionExtractJob:
    @patch("cognite.experimental.data_classes.vision.ContextualizationJob.result", new_callable=PropertyMock)
    @pytest.mark.parametrize(
        "status, result, expected_items",
        [
            (JobStatus.QUEUED, None, None),
            (
                JobStatus.COMPLETED,
                {"items": [{"fileId": 1, "annotations": mock_vision_predictions_dict}]},  # TODO: rename to predictions
                [VisionExtractItem(file_id=1, predictions=mock_vision_predictions_dict)],
            ),
        ],
        ids=["non_completed_job", "completed_job"],
    )
    def test_items_property(
        self, mock_result: MagicMock, status: JobStatus, result: Optional[Dict], expected_items: Optional[List]
    ) -> None:
        cognite_client = MagicMock(spec=CogniteClient)
        mock_result.return_value = result
        job = VisionExtractJob(status=status.value, cognite_client=cognite_client)
        assert job.items == expected_items

    @patch("cognite.experimental.data_classes.vision.ContextualizationJob.result", new_callable=PropertyMock)
    @pytest.mark.parametrize(
        "file_id, expected_item, error_message",
        [
            (1, VisionExtractItem(file_id=1, file_external_id="foo", predictions=mock_vision_predictions_dict), None),
            (1337, None, "File with id 1337 not found in results"),
        ],
        ids=["valid_unique_id", "non_existing_id"],
    )
    def test_get_item(
        self,
        mock_result: MagicMock,
        file_id: int,
        expected_item: Optional[VisionExtractItem],
        error_message: Optional[str],
    ) -> None:
        cognite_client = MagicMock(spec=CogniteClient)
        mock_result.return_value = {
            "items": [
                {
                    "fileId": i + 1,
                    "fileExternalId": "foo",
                    "annotations": mock_vision_predictions_dict,  # TODO: rename to predictions
                }
                for i in range(2)
            ]
        }
        job = VisionExtractJob(cognite_client=cognite_client)
        if error_message is not None:
            with pytest.raises(IndexError, match=error_message):
                job[file_id]
        else:
            assert job[file_id] == expected_item

    @patch("cognite.experimental.data_classes.vision.ContextualizationJob.result", new_callable=PropertyMock)
    @pytest.mark.parametrize(
        "result, params, expected_items",
        [
            (
                {"items": []},
                None,
                [],
            ),
            (
                {"items": [{"fileId": 1, "annotations": {}}]},
                None,
                [],
            ),
            (
                {"items": [{"fileId": 1, "annotations": {"text_annotations": []}}]},
                None,
                [],
            ),
            (
                {"items": [{"fileId": 1, "annotations": mock_vision_predictions_dict}]},  # TODO: rename to predictions
                {"creating_user": None, "creating_app": None, "creating_app_version": None},
                [
                    Annotation(
                        annotated_resource_id=1,
                        annotation_type="images.TextRegion",
                        data=resource_to_snake_case(mock_vision_predictions_dict)["text_annotations"][0],
                        annotated_resource_type="file",
                        status="suggested",
                        creating_app="cognite-sdk-experimental",
                        creating_app_version=1,
                        creating_user=None,
                    )
                ],
            ),
            (
                {"items": [{"fileId": 1, "annotations": mock_vision_predictions_dict}]},  # TODO: rename to predictions
                {"creating_user": "foo", "creating_app": "bar", "creating_app_version": "1.0.0"},
                [
                    Annotation(
                        annotated_resource_id=1,
                        annotation_type="images.TextRegion",
                        data=resource_to_snake_case(mock_vision_predictions_dict)["text_annotations"][0],
                        annotated_resource_type="file",
                        status="suggested",
                        creating_app="bar",
                        creating_app_version="1.0.0",
                        creating_user="foo",
                    )
                ],
            ),
        ],
        ids=[
            "empty_items",
            "empty_annotations",
            "empty_text_annotations",
            "completed_job_default_params",
            "completed_job_with_user_params",
        ],
    )
    def test_represent_predictions_as_annotations(
        self,
        mock_result: MagicMock,
        result: Optional[Dict],
        params: Optional[Dict],
        expected_items: Optional[List],
    ) -> None:
        cognite_client = MagicMock(spec=CogniteClient)
        cognite_client.version = (params or {}).get("creating_app_version") or 1
        mock_result.return_value = result
        job = VisionExtractJob(status=JobStatus.COMPLETED.value, cognite_client=cognite_client)
        assert job._represent_predictions_as_annotations(**(params or {})) == expected_items
