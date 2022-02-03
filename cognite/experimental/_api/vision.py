from typing import List, Optional, Union

from cognite.client._api_client import APIClient
from cognite.experimental.data_classes.vision import (
    IdEither,
    InternalId,
    DetectAssetsInFilesJob,
    CreatedDetectAssetsInFilesJob,
)


class VisionAPI(APIClient):
    _RESOURCE_PATH = "/context/vision"
    _TAG_DETECTION_PATH = "/tagdetection"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detect_assets_in_files(
        self,
        files: List[IdEither],
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
        return self._create_multiple(
            resource_path=self._RESOURCE_PATH + self._TAG_DETECTION_PATH + "/",
            items=files,
            extra_body_fields={
                "useCache": use_cache,
                "partialMatch": partial_match,
                "assetSubtreeIds": asset_subtree_ids,
            },
        )

    def retrieve_detected_assets_in_files_job(self, job_id: InternalId) -> DetectAssetsInFilesJob:
        """Retrieve detected external ID or name of assets with bounding boxes in images or single-page pdf files.

        Args:
            job_id (int): Contextualization job ID.

        Returns:
            DetectAssetsInFilesJob: job information with a list of succeeded and failed asset detection for files
        """
        return self._retrieve(
            id=job_id,
            resource_path=self._RESOURCE_PATH + self._TAG_DETECTION_PATH + "/",
        )
