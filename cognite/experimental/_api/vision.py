from typing import List, Optional, Union

from cognite.client._api_client import APIClient

from cognite.experimental.data_classes.vision import (
    CreatedDetectAssetsInFilesJob,
    DetectAssetsInFilesJob,
    EitherFileId,
    InternalId,
)
from cognite.experimental.utils import resource_to_camel_case


class VisionAPI(APIClient):
    _RESOURCE_PATH = "/context/vision"
    _TAG_DETECTION_PATH = f"{_RESOURCE_PATH}/tagdetection"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detect_assets_in_files(
        self,
        files: List[EitherFileId],
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
    ) -> CreatedDetectAssetsInFilesJob:
        """Initiate a job to detect external ID or name of assets in given file references

        Args:
            files (List[Union[int, str]]): references to files to work on
            use_cache (bool): uses cached result if the file has previously been analyzed.
            partial_match (bool): Allow partial (fuzzy) matching of detected external IDs in the file
            asset_subtree_ids (List[int]): Search for external ID or name of assets that are in a subtree rooted at one of the assetSubtreeIds

        Returns:
            DetectAssetsInFilesJob: job information
        """
        request = {
            "items": files,
            "use_cache": use_cache,
            "partial_match": partial_match,
            "asset_subtree_ids": asset_subtree_ids,
        }
        request = resource_to_camel_case(request)
        response = self._post(url_path=self._TAG_DETECTION_PATH, json=request)
        return CreatedDetectAssetsInFilesJob._load(response.json(), cognite_client=self._cognite_client)

    def retrieve_detected_assets_in_files_job(self, job_id: InternalId) -> DetectAssetsInFilesJob:
        """Retrieve detected external ID or name of assets with bounding boxes in images or single-page pdf files.

        Args:
            job_id (int): Contextualization job ID.

        Returns:
            DetectAssetsInFilesJob: job information with a list of succeeded and failed asset detection for files
        """
        return self._retrieve(id=job_id, resource_path=self._TAG_DETECTION_PATH, cls=DetectAssetsInFilesJob)
