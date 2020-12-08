from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI


class PNIDObjectDetectionAPI(ContextAPI):
    _RESOURCE_PATH = "/context/pnidobjects"

    def find_objects(self, file_id: int) -> ContextualizationJob:
        """Find objects in a PnID

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results.
        """
        return self._run_job(job_path="/findobjects", status_path="/findobjects/", file_id=file_id,)
