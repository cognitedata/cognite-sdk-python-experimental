from typing import Dict, List, cast

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList


class SimulationRun(CogniteResource):
    """Simulation run"""

    def __init__(
        self,
        simulator_name: str = None,
        model_name: str = None,
        routine_name: str = None,
        cognite_client: "CogniteClient" = None,
    ):
        self.simulator_name = simulator_name
        self.model_name = model_name
        self.routine_name = routine_name
        self._cognite_client = cast("CogniteClient", cognite_client)


class SimulationRunList(CogniteResourceList):
    _RESOURCE = SimulationRun
    _ASSERT_CLASSES = True
