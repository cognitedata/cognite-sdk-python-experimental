import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, cast, get_type_hints

from cognite.client import utils
from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.data_classes.contextualization import JobStatus
from typing_extensions import get_args

from cognite.experimental.data_classes import ContextualizationJobType
from cognite.experimental.data_classes.annotation_types.images import AssetLink, ObjectDetection, TextRegion
from cognite.experimental.utils import resource_to_camel_case, resource_to_snake_case

FeatureClass = Union[Type[TextRegion], Type[AssetLink], Type[ObjectDetection]]
ExternalId = str
InternalId = int


@dataclass
class ExternalFileId:
    file_external_id: ExternalId


@dataclass
class InternalFileId:
    file_id: InternalId


class Feature(str, Enum):
    TEXT_DETECTION = "TextDetection"
    ASSET_TAG_DETECTION = "AssetTagDetection"
    INDUSTRIAL_OBJECT_DETECTION = "IndustrialObjectDetection"
    PEOPLE_DETECTION = "PeopleDetection"
    PERSONAL_PROTECTIVE_EQUIPMENT_DETECTION = "PersonalProtectiveEquipmentDetection"


@dataclass
class AnnotatedObject:
    text_annotations: Optional[List[TextRegion]] = None
    asset_tag_annotations: Optional[List[AssetLink]] = None
    industrial_object_annotations: Optional[List[ObjectDetection]] = None
    people_annotations: Optional[List[ObjectDetection]] = None
    personal_protective_equipment_annotations: Optional[List[ObjectDetection]] = None

    @staticmethod
    def _get_feature_class(type_hint: Type[Optional[List[FeatureClass]]]) -> FeatureClass:
        # Unwrap the first level of type hints (i.e., the Optional[...])
        # NOTE: outer type hint MUST be an Optional, since Optional[X] == Union[X, None]
        list_type_hint, _ = get_args(type_hint)
        # Unwrap the second level of type hint (i.e., the List[...])
        (class_type,) = get_args(list_type_hint)
        return class_type


# Auto-generate the annotation-to-dataclass mapping based on the type hints of AnnotatedObject
VISION_FEATURE_MAP: Dict[str, FeatureClass] = {
    key: AnnotatedObject._get_feature_class(value) for key, value in get_type_hints(AnnotatedObject).items()
}

EitherFileId = Union[InternalFileId, ExternalFileId]


@dataclass
class AllOfFileId(InternalFileId):
    file_external_id: Optional[ExternalId] = None


class VisionJob(ContextualizationJob):
    def update_status(self) -> str:
        # Override update_status since we need to handle the vision-specific
        # edge case where we also record failed items per batch
        data = (
            self._cognite_client.__getattribute__(self._JOB_TYPE.value)._get(f"{self._status_path}{self.job_id}").json()
        )
        self.status = data["status"]
        self.status_time = data.get("statusTime")
        self.start_time = data.get("startTime")
        self.created_time = self.created_time or data.get("createdTime")
        self.error_message = data.get("errorMessage") or data.get("failedItems")
        self._result = {k: v for k, v in data.items() if k not in self._COMMON_FIELDS}
        assert self.status is not None
        return self.status


class CreatedDetectAssetsInFilesJob(CogniteResource):
    def __init__(
        self,
        status: JobStatus,
        created_time: int,
        status_time: int,
        job_id: int,
        items: Optional[List[AllOfFileId]] = None,
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
        start_time: Optional[int] = None,
    ) -> None:
        self.status = status
        self.created_time = created_time
        self.status_time = status_time
        self.job_id = job_id
        self.use_cache = use_cache
        self.partial_match = partial_match
        self.asset_subtree_ids = asset_subtree_ids
        self.start_time = start_time
        self.items = items

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        if camel_case:
            return resource_to_camel_case(self)
        else:
            return resource_to_snake_case(self)

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        if isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            instance = cls(
                status=k["status"],
                created_time=k["created_time"],
                status_time=k["status_time"],
                job_id=k["job_id"],
                use_cache=k.get("use_cache"),
                partial_match=k.get("partial_match"),
                asset_subtree_ids=k.get("asset_subtree_ids"),
            )
            items = k.get("items")
            if items is not None:
                instance.items = [
                    AllOfFileId(file_id=item["file_id"], file_external_id=item.get("file_external_id"))
                    for item in k["items"]
                ]
            return instance

        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


@dataclass
class FailedAssetDetectionInFiles:
    error_message: str
    items: List[AllOfFileId]

    @classmethod
    def _load(cls, resource: Optional[Union[Dict, str]] = None):
        if resource is None:
            return None
        elif isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            return cls(
                error_message=k["error_message"],
                items=[
                    AllOfFileId(file_id=v["file_id"], file_external_id=v.get("file_external_id")) for v in k["items"]
                ],
            )
        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


@dataclass
class VisionVertex:
    x: float
    y: float


@dataclass
class VisionRegion:
    shape: str
    vertices: List[VisionVertex]

    @classmethod
    def _load(cls, resource: Optional[Union[Dict, str]] = None):
        if resource is None:
            return None
        elif isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            return cls(
                shape=k["shape"],
                vertices=[VisionVertex(x=v["x"], y=v["y"]) for v in k["vertices"]],
            )
        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


@dataclass
class VisionTagDetectionAnnotation:
    text: str
    asset_ids: List[InternalId]
    confidence: Optional[float] = None
    region: Optional[VisionRegion] = None

    @classmethod
    def _load(cls, resource: Optional[Union[Dict, str]] = None):
        if resource is None:
            return None
        elif isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            return cls(
                text=k["text"],
                asset_ids=k["asset_ids"],
                confidence=k.get("confidence"),
                region=VisionRegion._load(k.get("region")),
            )
        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


@dataclass
class SuccessfulAssetDetectionInFiles(AllOfFileId):
    width: Optional[int] = None
    height: Optional[int] = None
    annotations: Optional[List[VisionTagDetectionAnnotation]] = None

    @classmethod
    def _load(cls, resource: Union[Dict, str]):
        if isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            instance = cls(
                file_id=k["file_id"],
                file_external_id=k.get("file_external_id"),
                width=k.get("width"),
                height=k.get("height"),
            )
            annotations = k.get("annotations")
            if annotations is not None:
                instance.annotations = [VisionTagDetectionAnnotation._load(v) for v in annotations]
            return instance
        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


class DetectAssetsInFilesJob(CogniteResource):
    def __init__(
        self,
        status: JobStatus,
        created_time: int,
        status_time: int,
        job_id: int,
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
        start_time: Optional[int] = None,
        items: Optional[List[SuccessfulAssetDetectionInFiles]] = None,
        failed_items: Optional[List[FailedAssetDetectionInFiles]] = None,
    ) -> None:
        self.status = status
        self.created_time = created_time
        self.status_time = status_time
        self.job_id = job_id
        self.use_cache = use_cache
        self.partial_match = partial_match
        self.asset_subtree_ids = asset_subtree_ids
        self.start_time = start_time
        self.items = items
        self.failed_items = failed_items

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        if camel_case:
            return resource_to_camel_case(self)
        else:
            return resource_to_snake_case(self)

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        if isinstance(resource, str):
            return cls._load(json.loads(resource))
        elif isinstance(resource, Dict):
            k = resource_to_snake_case(resource)
            instance = cls(
                status=k["status"],
                created_time=k["created_time"],
                status_time=k["status_time"],
                job_id=k["job_id"],
                use_cache=k.get("use_cache"),
                partial_match=k.get("partial_match"),
                asset_subtree_ids=k.get("asset_subtree_ids"),
            )
            failed_items = k.get("failed_items")
            if failed_items is not None:
                instance.failed_items = [FailedAssetDetectionInFiles._load(v) for v in failed_items]
            successful_items = k.get("items")
            if successful_items is not None:
                instance.items = [SuccessfulAssetDetectionInFiles._load(v) for v in successful_items]
            return instance
        raise TypeError(f"Resource must be json str or Dict, not {type(resource)}")


class AnnotatedItem(CogniteResource):
    def __init__(
        self,
        file_id: int = None,
        annotations: Dict[str, Any] = None,
        file_external_id: str = None,
        error_message: str = None,
        cognite_client: "CogniteClient" = None,
    ) -> None:
        """Data class for storing a single annotated item"""
        self.file_id = file_id
        self.file_external_id = file_external_id
        self.error_message = error_message
        self.annotations = self._process_annotations_dict(annotations) if isinstance(annotations, Dict) else annotations

        self._annotations_dict = annotations  # The "raw" annotations dict returned by the endpoint
        self._cognite_client = cast("CogniteClient", cognite_client)

    @classmethod
    def _load(cls: "AnnotatedItem", resource: Union[Dict, str], cognite_client: "CogniteClient" = None):
        """Override CogniteResource._load so that we can convert the dicts returned by the API to data classes"""
        annotated_item = super(AnnotatedItem, cls)._load(resource, cognite_client=cognite_client)
        if annotated_item.annotations is not None:
            annotated_item._annotations_dict = annotated_item.annotations
            annotated_item.annotations = cls._process_annotations_dict(annotated_item._annotations_dict)
        return annotated_item

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        item_dump = super().dump(camel_case=camel_case)
        # Replace the loaded AnnotationObject with its corresponding dict representation
        if "annotations" in item_dump and isinstance(self._annotations_dict, Dict):
            item_dump["annotations"] = (
                self._annotations_dict if camel_case else resource_to_snake_case(self._annotations_dict)
            )
        return item_dump

    @staticmethod
    def _process_annotations_dict(annotations_dict: Dict[str, Any]) -> AnnotatedObject:
        """Converts a (validated) annotations dict to a corresponding AnnotatedObject"""
        annotated_object = AnnotatedObject()
        snake_case_annotations_dict = resource_to_snake_case(annotations_dict)
        for key, value in snake_case_annotations_dict.items():
            if hasattr(annotated_object, key):
                feature_class = VISION_FEATURE_MAP[key]
                setattr(annotated_object, key, [feature_class(**v) for v in value])
        return annotated_object


class AnnotatedItemList(CogniteResourceList):
    _RESOURCE = AnnotatedItem
    _UPDATE = AnnotatedItem


class AnnotateJobResults(VisionJob):
    _JOB_TYPE = ContextualizationJobType.VISION

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._items: Optional[List[AnnotatedItemList]] = None

    def __getitem__(self, file_id: InternalId) -> AnnotatedItem:
        """Retrieves the results for a file by (external) id"""
        found = [item for item in self.result["items"] if item.get("fileId") == file_id]
        if not found:
            raise IndexError(f"File with id {file_id} not found in results")
        return AnnotatedItem._load(found[0], cognite_client=self._cognite_client)

    @property
    def items(self) -> Optional[AnnotatedItemList]:
        """Returns a list of all annotate results by file"""
        if self.status == JobStatus.COMPLETED.value:
            self._items = AnnotatedItemList._load(self.result["items"], cognite_client=self._cognite_client)
        return self._items

    @items.setter
    def items(self, items: List[Union[List[AnnotatedItem], AnnotatedItemList]]) -> None:
        self._items = items

    @property
    def errors(self) -> List[str]:
        """Returns a list of all error messages across files"""
        return [item["errorMessage"] for item in self.result["items"] if "errorMessage" in item]
