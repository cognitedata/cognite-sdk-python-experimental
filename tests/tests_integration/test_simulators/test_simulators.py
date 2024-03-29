import os
import time

from pytest import fixture, mark

from cognite.client import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.utils._logging import _configure_logger_for_debug_mode
from cognite.experimental import CogniteClient
from cognite.experimental.data_classes.simulators import SimulationRun


@fixture(scope="class")
def cognite_client() -> CogniteClient:
    _configure_logger_for_debug_mode()
    creds = OAuthClientCredentials(
        token_url=os.environ["COGNITE_TOKEN_URL"],
        client_id=os.environ["COGNITE_CLIENT_ID"],
        client_secret=os.environ["COGNITE_CLIENT_SECRET"],
        scopes=[os.environ["COGNITE_TOKEN_SCOPES"]],
    )
    return CogniteClient(
        config=ClientConfig(
            base_url=os.environ["COGNITE_BASE_URL"],
            client_name="experimental",
            project="charts-azuredev",
            headers={"cdf-version": "alpha"},
            credentials=creds,
        )
    )


@mark.skipif(
    os.environ.get("ENABLE_SIMULATORS_TESTS") is None, reason="Skipping simulators API tests due to service immaturity"
)
class TestSimulatorsIntegration:
    def test_run_single_simulation(self, cognite_client: CogniteClient):
        now = int(round(time.time() * 1000))
        test_run = SimulationRun(
            simulator_name="DWSIM",
            model_name="ShowerMixerIntegrationTest",
            routine_name="ShowerMixerCalculation",
            validation_end_time=now,
            queue=False,
        )
        res = cognite_client.simulators.run(test_run)

        assert isinstance(res, SimulationRun)
        assert res.simulator_name == test_run.simulator_name
        assert res.model_name == test_run.model_name
        assert res.routine_name == test_run.routine_name
        assert res.validation_end_time == test_run.validation_end_time
        assert res.queue is None
        assert res.id is not None
        assert res.created_time is not None

    def test_list_simulation_runs(self, cognite_client: CogniteClient):
        res = cognite_client.simulators.list_runs(
            simulator_name="DWSIM",
            model_name="ShowerMixerIntegrationTest",
            routine_name="ShowerMixerCalculation",
            status="ready",
        )

        assert len(res) > 0
        assert res[0].simulator_name == "DWSIM"
        assert res[0].status == "ready"
        assert res[0].created_time > 0
