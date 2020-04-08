import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
EEAPI = COGNITE_CLIENT.entity_extraction


class TestEntityExtractionIntegration:
    def test_run_fails(self):
        job = EEAPI.extract([1], [])
        with pytest.raises(ModelFailedException) as exc_info:
            job.result
        assert "failed with error" in str(exc_info.value)
