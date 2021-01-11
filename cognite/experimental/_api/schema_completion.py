from typing import Dict, List

from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI


class SchemaCompletionAPI(ContextAPI):
    _RESOURCE_PATH = "/context/schemas"

    def complete_type(self, external_id: str) -> ContextualizationJob:
        """Completes a schema uploaded in CDF as a type.

        Args:
            external_id (str): External ID of the type to be completed

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(job_path="/type", status_path="/", external_id=external_id)

    def complete_domain(
        self, external_id: str, template_name: str, asset_property: str, version: int = None
    ) -> ContextualizationJob:
        """Completes a schema uploaded in CDF as a domain.

        Args:
            external_id (str), version (int): External ID of the domain to work on, with optional version.
            template_name: Name of the template to be completed within the domain
            asset_property: Which field (with constant type) in the template defines the externalId of the parent asset in each entry.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        return self._run_job(
            job_path="/domain",
            status_path="/",
            external_id=external_id,
            template_name=template_name,
            asset_property=asset_property,
            version=version,
        )
