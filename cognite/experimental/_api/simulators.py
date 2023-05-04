from typing import Dict, List, Union

from cognite.client._api_client import APIClient
from cognite.client.utils._auxiliary import assert_type

from cognite.experimental.data_classes.simulators import SimulationRun, SimulationRunList


class SimulationRunsAPI(APIClient):
    _RESOURCE_PATH = "/simulators/run"
    _LIST_CLASS = SimulationRunList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(
        self,
        items: Union[SimulationRun, List[SimulationRun]],
    ) -> Union[SimulationRun, SimulationRunList]:
        """Run a simulation

        Args:
            items (Union[SimulationRun, List[SimulationRun]]): simulation(s) to run

        Returns:
            Union[SimulationRun, SimulationRunList]: simulation run(s)
        """
        assert_type(items, "items", [SimulationRun, list])
        return self._create_multiple(
            items=items,
            resource_path=self._RESOURCE_PATH,
            list_cls=SimulationRunList,
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
        return self.simulations.run(items)
