import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing


class TestPNIDParsingIntegration:
    def test_run_fails(self):
        job = PNIDAPI.parse(1, [])
        with pytest.raises(ModelFailedException) as exc_info:
            job.result
        assert "failed with error" in str(exc_info.value)
