import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from cognite.client.data_classes._base import CogniteResource
from cognite.client.utils._auxiliary import to_snake_case

ExternalId = str
InternalId = int
IdEither = Union[InternalId, ExternalId]


@dataclass
class EitherFileId:
    file_id: InternalId
    file_external_id: Optional[ExternalId] = None


class JobStatus(str, Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


class _DetectedAssetsInFilesJob(CogniteResource):
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
    ) -> None:
        self.status = status
        self.created_time = created_time
        self.status_time = status_time
        self.job_id = job_id
        self.use_cache = use_cache
        self.partial_match = partial_match
        self.asset_subtree_ids = asset_subtree_ids
        self.start_time = start_time


class CreatedDetectAssetsInFilesJob(_DetectedAssetsInFilesJob):
    def __init__(
        self,
        items: List[EitherFileId],
        status: JobStatus,
        created_time: int,
        status_time: int,
        job_id: int,
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
        start_time: Optional[int] = None,
    ) -> None:
        super().__init__(
            status=status,
            created_time=created_time,
            status_time=status_time,
            job_id=job_id,
            use_cache=use_cache,
            partial_match=partial_match,
            asset_subtree_ids=asset_subtree_ids,
            start_time=start_time,
        )
        self.items = items

    @classmethod
    def from_dict(cls, resource: Dict[str, Any], cognite_client=None) -> "CreatedDetectAssetsInFilesJob":
        data = {to_snake_case(key): val for key, val in resource.items()}
        job = cls(**data)
        job._cognite_client = cognite_client
        return job

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        result = super().dump(camel_case=camel_case)
        return result


@dataclass
class FailedAssetDetectionInFiles:
    error_message: str
    items: List[EitherFileId]


@dataclass
class VisionVertex:
    x: float
    y: float


@dataclass
class VisionRegion:
    shape: str
    vertices: List[VisionVertex]


@dataclass
class VisionTagDetectionAnnotation:
    text: str
    asset_ids: List[InternalId]
    confidence: Optional[float] = None
    region: Optional[VisionRegion] = None


@dataclass
class SuccessfulAssetDetectionInFiles:
    file_id: InternalId
    file_external_id: Optional[ExternalId] = None
    width: Optional[int] = None
    height: Optional[int] = None
    annotations: Optional[List[VisionTagDetectionAnnotation]] = None


class DetectAssetsInFilesJob(_DetectedAssetsInFilesJob):
    def __init__(
        self,
        items: List[SuccessfulAssetDetectionInFiles],
        status: JobStatus,
        created_time: int,
        status_time: int,
        job_id: int,
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
        start_time: Optional[int] = None,
        failed_items: Optional[List[FailedAssetDetectionInFiles]] = None,
    ) -> None:
        super().__init__(
            status=status,
            created_time=created_time,
            status_time=status_time,
            job_id=job_id,
            use_cache=use_cache,
            partial_match=partial_match,
            asset_subtree_ids=asset_subtree_ids,
            start_time=start_time,
        )
        self.items = items
        self.failed_items = failed_items

    @classmethod
    def _load(cls, resource: Union[Dict[str, Any], str], cognite_client=None) -> "DetectAssetsInFilesJob":
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client=cognite_client)
        elif isinstance(resource, dict):
            return cls.from_dict(resource, cognite_client=cognite_client)
        raise TypeError("Resource must be json str or Dict, not {}".format(type(resource)))

    @classmethod
    def from_dict(cls, resource: Dict[str, Any], cognite_client=None) -> "DetectAssetsInFilesJob":
        data = {to_snake_case(key): val for key, val in resource.items()}
        job = cls(**data)
        job._cognite_client = cognite_client
        return job

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        result = super().dump(camel_case=camel_case)
        return result
