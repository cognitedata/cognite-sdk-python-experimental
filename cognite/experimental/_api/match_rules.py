from typing import Dict, List, Union

from cognite.client import utils

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import EntityMatchingMatchRuleList, MatchRulesApplyJob, MatchRulesSuggestJob


class MatchRulesAPI(ContextAPI):
    _RESOURCE_PATH = "/context/matchrules"

    def apply(
        self, sources: List[dict], targets: List[dict], rules: Union[List[dict], EntityMatchingMatchRuleList]
    ) -> MatchRulesApplyJob:
        """Apply match rules with priorities to match source entities with target entities.

        Args:
            sources (List[dict]): List of source entities in json format.
            targets (List[dict]): List of target entities in json format.
            rules (Union[List[dict], EntityMatchingMatchruleList]): List of match rules with priorities to apply to the
                entities
        Returns:
            MatchRulesApplyJob: Job, calling .rules waits for completion."""

        if isinstance(rules, EntityMatchingMatchRuleList):
            rules = [
                {k: r.dump()[k] for k in ["extractors", "conditions", "priority"] if r.dump().get(k)}
                for r in rules.data
            ]

        return self._run_job(
            job_path="/apply",
            status_path="/apply/",
            sources=sources,
            targets=targets,
            rules=rules,
            job_cls=MatchRulesApplyJob,
        )

    def suggest(self, sources: List[dict], targets: List[dict], matches: List[dict]) -> MatchRulesSuggestJob:
        """Suggest match rules with priorities based on existing matches between source and target entities.

        Args:
            sources (List[dict]): List of dict representation of source entities to suggest rules for.
            targets (List[dict]): List of dict representation of target entities to suggest rules for.
            matches (list[dict]): List of matches in terms of source_id or source_external_id and similar for target.

        Returns:
            MatchRulesSuggestJob: Resulting queued job. Note that .rules property of this job will block waiting for
            results.
        """
        matches = [{utils._auxiliary.to_camel_case(k): v for k, v in match.items()} for match in matches]
        return self._run_job(
            job_path="/suggest",
            status_path="/suggest/",
            sources=sources,
            targets=targets,
            matches=matches,
            job_cls=MatchRulesSuggestJob,
        )
