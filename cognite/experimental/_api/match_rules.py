from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import PriorityRuleList


class MatchRulesAPI(ContextAPI):
    _RESOURCE_PATH = "/context/matchrules"

    def apply(
        self,
        sources: List[dict],
        targets: List[dict],
        priority_rules: Union[dict, PriorityRuleList],
    ) -> ContextualizationJob:
        """Apply match rules with priorities to source entities with target entities.

        Args:
            sources (List[dict]): List of source entities in json format.
            targets (List[dict]): List of target entities in json format.
            priority_rules (Union[dict, PriorityRuleList]): List of match rules with priorities to apply to the entities
        Returns:
            ContextualizationJob: Resulting completed job. Note that this function waits for completion."""

        job = self._run_job(
            job_path="/apply",
            status_path="/apply/",
            sources=sources,
            targets=targets,
            priority_rules=priority_rules,
        )
        return job

    def suggest(
        self, sources: List[dict], targets: List[dict], matches: List[dict],
    ) -> ContextualizationJob:
        """Extract tags from P&ID based on pattern

        Args:
            file_id (int): ID of the file, should already be uploaded in the same tenant.
            patterns (list): List of regular expression patterns to look for in the P&ID. See API docs for details.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        return self._run_job(
            job_path="/suggest",
            status_path="/suggest/",
            souorces=sources,
            targets=targets,
            patterns=matches,
        )
