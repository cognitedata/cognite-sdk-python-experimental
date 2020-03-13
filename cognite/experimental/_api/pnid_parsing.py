from typing import Dict, List

from cognite.experimental._context_client import ContextAPI
from cognite.experimental.data_classes import ContextualizationJob


class PNIDParsingAPI(ContextAPI):
    _RESOURCE_PATH = "/context/pnid"

    def run(
        self, file_id: int, entities: List[str], name_mapping: Dict[str, str] = None, partial_match: bool = False
    ) -> "Task[ContextualizationJob]":
        return self._run_job(
            job_path="/parse",
            file_id=file_id,
            entities=entities,
            partial_match=partial_match,
            name_mapping=name_mapping,
        )
