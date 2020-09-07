import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing


class TestPNIDParsingIntegration:
    def test_run_fails(self):
        entities = ["a", "b"]
        file_id = 123432423
        job = PNIDAPI.detect(file_id, entities, name_mapping={"a": "c"}, partial_match=False, min_tokens=3)
        with pytest.raises(ModelFailedException) as exc_info:
            job.result
        assert "failed with error" in str(exc_info.value)
