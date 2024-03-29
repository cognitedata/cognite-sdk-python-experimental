from __future__ import annotations

from typing import TYPE_CHECKING, cast

from cognite.client.data_classes._base import CogniteFilter, CogniteResource, CogniteResourceList

if TYPE_CHECKING:
    from cognite.experimental import CogniteClient


class SimulationRun(CogniteResource):
    """Simulation run

    Args:
        id (int): ID of the simulation run
        simulator_name (str): name of the simulator
        model_name (str): name of the model
        routine_name (str): name of the routine
        status (str): status of the simulation run. One of ("ready", "running", "success", "failure")
        status_message (str): status message of the simulation run
        validation_end_time (int): validation end time of the simulation run
        queue (bool): whether the simulation run is queued
        created_time (int): created time of the simulation run
        last_updated_time (int): last updated time of the simulation run

    """

    def __init__(
        self,
        id: int | None = None,
        simulator_name: str | None = None,
        model_name: str | None = None,
        routine_name: str | None = None,
        status: str | None = None,
        status_message: str | None = None,
        validation_end_time: int | None = None,
        queue: bool | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
        cognite_client: CogniteClient = None,
    ):
        self.id = id
        self.simulator_name = simulator_name
        self.model_name = model_name
        self.routine_name = routine_name
        self.status = status
        self.status_message = status_message
        self.validation_end_time = validation_end_time
        self.queue = queue
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cast("CogniteClient", cognite_client)


class SimulationRunList(CogniteResourceList):
    """List of simulation runs"""

    _RESOURCE = SimulationRun
    _ASSERT_CLASSES = True


class SimulationRunFilter(CogniteFilter):
    """Filter simulation runs with strict matching.

    Args:
        simulator_name (str): name of the simulator
        model_name (str): name of the model
        routine_name (str): name of the routine
        status (str): status of the simulation run. One of ("ready", "running", "success", "failure")

    """

    def __init__(
        self,
        simulator_name: str | None = None,
        model_name: str | None = None,
        routine_name: str | None = None,
        status: str | None = None,
        cognite_client: CogniteClient | None = None,
    ):
        self.simulator_name = simulator_name
        self.model_name = model_name
        self.routine_name = routine_name
        self.status = status
        self._cognite_client = cast("CogniteClient", cognite_client)
