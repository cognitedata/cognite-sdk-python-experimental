import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
PNIDAPI = COGNITE_CLIENT.pnid_parsing


class TestPNIDParsingIntegration:
    @pytest.mark.asyncio
    async def test_run_fails(self):
        task = PNIDAPI.parse(1, [])
        with pytest.raises(ModelFailedException) as exc_info:
            await task
        assert "failed with error" in str(exc_info.value)
