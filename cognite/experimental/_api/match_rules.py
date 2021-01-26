from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import MatchRule


class MatchRulesAPI(ContextAPI):
    _RESOURCE_PATH = "/context/matchrules"

    def apply(
        self, sources: List[dict], targets: List[dict], rules: List[Union[dict, MatchRule]],
    ) -> ContextualizationJob:
        """Apply match rules with priorities to source entities with target entities.

        Args:
            sources (List[dict]): List of source entities in json format.
            targets (List[dict]): List of target entities in json format.
            priority_rules (Union[dict, PriorityRuleList]): List of match rules with priorities to apply to the entities
        Returns:
            ContextualizationJob: Resulting completed job. Note that this function waits for completion."""

        job = self._run_job(job_path="/apply", status_path="/apply/", sources=sources, targets=targets, rules=rules,)
        return job

    def suggest(self, sources: List[dict], targets: List[dict], matches: List[dict],) -> ContextualizationJob:
        """Extract tags from P&ID based on pattern

        Args:
            sources (List[dict]): List of dict representation of source entities to suggest rules for.
            targets (List[dict]): List of dict representation of target entities to suggest rules for.
            matches (list[dict]): List of matches in terms of source_id or source_external_id and similar for target.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""

        return self._run_job(
            job_path="/suggest", status_path="/suggest/", sources=sources, targets=targets, matches=matches,
        )
