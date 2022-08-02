from typing import List, Optional, Union

from cognite.client.utils._auxiliary import assert_type

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes.vision import (
    AnnotateJobResults,
    CreatedDetectAssetsInFilesJob,
    DetectAssetsInFilesJob,
    EitherFileId,
    Feature,
    InternalId,
)
from cognite.experimental.utils import resource_to_camel_case


class VisionAPI(ContextAPI):
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
            CreatedDetectAssetsInFilesJob: job information
        """
        request = self._prepare_detect_assets_in_files_request(files, use_cache, partial_match, asset_subtree_ids)
        response = self._post(url_path=self._TAG_DETECTION_PATH, json=request)
        return CreatedDetectAssetsInFilesJob._load(response.json(), cognite_client=self._cognite_client)

    @classmethod
    def _prepare_detect_assets_in_files_request(
        cls,
        files: List[EitherFileId],
        use_cache: Optional[bool] = None,
        partial_match: Optional[bool] = None,
        asset_subtree_ids: Optional[List[InternalId]] = None,
    ) -> dict:
        request = {
            "items": files,
            "use_cache": use_cache,
            "partial_match": partial_match,
            "asset_subtree_ids": asset_subtree_ids,
        }
        request = resource_to_camel_case(request)
        return request

    def retrieve_detected_assets_in_files_job(self, job_id: InternalId) -> DetectAssetsInFilesJob:
        """Retrieve detected external ID or name of assets with bounding boxes in images or single-page pdf files.

        Args:
            job_id (int): Contextualization job ID.

        Returns:
            DetectAssetsInFilesJob: job information with a list of succeeded and failed asset detection for files
        """
        return self._retrieve(id=job_id, resource_path=self._TAG_DETECTION_PATH, cls=DetectAssetsInFilesJob)

    def annotate(
        self,
        features: Union[Feature, List[Feature]],
        file_ids: Optional[List[int]] = None,
        file_external_ids: Optional[List[str]] = None,
    ) -> AnnotateJobResults:
        """Annotate image files with a provided set of feature(s).

        Args:
            features (Union[Feature, List[Feature]]): The feature(s) to extract from the provided image files.
            file_ids (List[int]): IDs of the image files to annotate. The images must already be uploaded in the same CDF project.
            file_external_ids (List[str]): The external file ids of the image files to annotate
        Returns:
            AnnotateJobResults: Resulting queued job, which can be used to retrieve the status of the job or the annotation results if the job is finished. Note that .result property of this job will wait for the job to finish and returns the results.

        Examples:
            Start a job, wait for completion and then get the parsed results::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.vision import Feature
                >>> c = CogniteClient()
                >>> annotate_job = c.vision.annotate(features=Feature.ASSET_TAG_DETECTION, file_ids=[1])
                >>> annotate_job.wait_for_completion()
                >>> for item in annotate_job.items:
                ...     annotations = item.annotations
                ...     # do something with the annotations
        """
        # Sanitize input(s)
        assert_type(features, "features", [Feature, list], allow_none=False)
        if isinstance(features, list):
            for f in features:
                assert_type(f, f"feature '{f}'", [Feature], allow_none=False)
        if isinstance(features, Feature):
            features = [features]

        return self._run_job(
            job_path="/annotate",
            status_path="/annotate/",
            items=self._process_file_ids(file_ids, file_external_ids),
            features=features,
            job_cls=AnnotateJobResults,
        )
