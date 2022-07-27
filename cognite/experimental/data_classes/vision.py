import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union, cast

from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.client.data_classes.contextualization import JobStatus

from cognite.experimental.data_classes import ContextualizationJobType
from cognite.experimental.utils import resource_to_camel_case, resource_to_snake_case

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
    PPE_DETECTION = "PersonalProtectiveEquipmentDetection"


EitherFileId = Union[InternalFileId, ExternalFileId]


@dataclass
class AllOfFileId(InternalFileId):
    file_external_id: Optional[ExternalId] = None


class VisionJob(ContextualizationJob):
    def update_status(self) -> str:
        # Handle the vision-specific edge case where we also record failed items per batch
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
        self.file_id = file_id
        self.file_external_id = file_external_id
        self.annotations = annotations
        self.error_message = error_message
        self._cognite_client = cast("CogniteClient", cognite_client)


class AnnotatedItemList(CogniteResourceList):
    _RESOURCE = AnnotatedItem
    _UPDATE = AnnotatedItem


class AnnotateJobResults(VisionJob):
    _JOB_TYPE = ContextualizationJobType.VISION

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._items: Optional[List[AnnotatedItemList]] = None

    def __getitem__(self, find_id: EitherFileId) -> AnnotatedItem:
        """retrieves the results for the file with (external) id"""
        found = [
            item
            for item in self.result["items"]
            if item.get("fileId") == find_id or item.get("fileExternalId") == find_id
        ]
        if not found:
            raise IndexError(f"File with (external) id {find_id} not found in results")
        if len(found) != 1:
            raise IndexError(f"Found multiple results for file with (external) id {find_id}, use .items instead")
        return AnnotatedItem._load(found[0], cognite_client=self._cognite_client)

    @property
    def items(self) -> Optional[AnnotatedItemList]:
        """returns a list of all results by file"""
        if self.status == JobStatus.COMPLETED.value:
            self._items = AnnotatedItemList._load(self.result["items"], cognite_client=self._cognite_client)
        return self._items

    @items.setter
    def items(self, items: List[Union[List[AnnotatedItem], AnnotatedItemList]]) -> None:
        self._items = items

    @property
    def errors(self) -> List[str]:
        """returns a list of all error messages across files"""
        return [item["errorMessage"] for item in self.result["items"] if "errorMessage" in item]
