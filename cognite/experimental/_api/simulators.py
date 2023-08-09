from typing import Dict, List, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type

from cognite.experimental.data_classes.simulators import SimulationRun, SimulationRunFilter, SimulationRunList


class SimulationRunsAPI(APIClient):
    _RESOURCE_PATH = "/simulators/run"
    _LIST_CLASS = SimulationRunList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(
        self,
        items: Union[SimulationRun, List[SimulationRun]],
    ) -> Union[SimulationRun, SimulationRunList]:
        assert_type(items, "items", [SimulationRun, list])
        return self._create_multiple(
            items=items,
            resource_path=self._RESOURCE_PATH,
            list_cls=SimulationRunList,
            resource_cls=SimulationRun,
        )

    def list_runs(
        self,
        simulator_name: str = None,
        model_name: str = None,
        routine_name: str = None,
        status: str = None,
    ) -> SimulationRunList:
        filter = SimulationRunFilter(
            simulator_name=simulator_name,
            model_name=model_name,
            routine_name=routine_name,
            status=status,
        ).dump(camel_case=True)

        return self._list(
            method="POST",
            filter=filter,
            list_cls=SimulationRunList,
            resource_path="/simulators/runs",
            resource_cls=SimulationRun,
        )


class SimulatorsAPI(APIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simulations = SimulationRunsAPI(*args, **kwargs)

    def run(
        self,
        items: Union[SimulationRun, List[SimulationRun]],
    ) -> Union[SimulationRun, SimulationRunList]:
        """Run a simulation

        Args:
            items (Union[SimulationRun, List[SimulationRun]]): simulation(s) to run

        Returns:
            Union[SimulationRun, SimulationRunList]: simulation run(s)

        Examples:

            Run a simulation::

                >>> from cognite.experimental import CogniteClient
                >>> from cognite.experimental.data_classes.simulators import SimulationRun
                >>> c = CogniteClient()
                >>> client.config.headers = {"cdf-version": "alpha"}
                >>> test_run = SimulationRun(simulator_name="my_simulator", model_name="my_model", routine_name="my_routine")
                >>> c.simulators.run(items=test_run)
        """
        return self.simulations.run(items)

    def list_runs(
        self,
        simulator_name: str = None,
        model_name: str = None,
        routine_name: str = None,
        status: str = None,
    ) -> SimulationRunList:
        """List simulation runs

        Args:
            simulator_name: name of the simulator
            model_name: name of the model
            routine_name: name of the routine
            status: status of the simulation run. One of ("ready", "running", "success", "failure")

        Returns:
            SimulationRunList: list of simulation runs

        Examples:

            List simulation runs::

                >>> from cognite.experimental import CogniteClient
                >>> c = CogniteClient()
                >>> client.config.headers = {"cdf-version": "alpha"}
                >>> c.simulators.list_runs(
                >>>     simulator_name="my_simulator", model_name="my_model", routine_name="my_routine", status="success"
                >>> )
        """
        return self.simulations.list_runs(
            simulator_name=simulator_name, model_name=model_name, routine_name=routine_name, status=status
        )
