import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from cognite.client.data_classes._base import CogniteResource
from cognite.client.data_classes.contextualization import JobStatus

from cognite.experimental.utils import resource_to_camel_case, resource_to_snake_case

ExternalId = str
InternalId = int


@dataclass
class ExternalFileId:
    file_external_id: ExternalId


@dataclass
class InternalFileId:
    file_id: InternalId


EitherFileId = Union[InternalFileId, ExternalFileId]


@dataclass
class AllOfFileId(InternalFileId):
    file_external_id: Optional[ExternalId] = None


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
        assert camel_case
        return resource_to_camel_case(self)

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
            return cls(shape=k["shape"], vertices=[VisionVertex(x=v["x"], y=v["y"]) for v in k["vertices"]],)
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
        assert camel_case
        return resource_to_camel_case(self)

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
