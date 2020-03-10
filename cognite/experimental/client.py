from cognite.client._api.datapoints import DatapointsAPI
from cognite.client._api.synthetic_time_series import SyntheticDatapointsAPI
from cognite.client._cognite_client import CogniteClient as Client
from cognite.experimental._api.assets import ExperimentalAssetsAPI
from cognite.experimental._api.model_hosting import ModelHostingAPI
from cognite.experimental._api.relationships import RelationshipsAPI
from cognite.experimental._api.types import TypesAPI


class ExperimentalDatapointsApi(DatapointsAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synthetic = SyntheticDatapointsAPI(self._config, api_version="playground", cognite_client=self)


class CogniteClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relationships = RelationshipsAPI(self._config, api_version="playground", cognite_client=self)
        self.datapoints = ExperimentalDatapointsApi(self._config, api_version="v1", cognite_client=self)
        self.model_hosting = ModelHostingAPI(self._config, api_version="playground", cognite_client=self)
        self.assets = ExperimentalAssetsAPI(self._config, api_version="playground", cognite_client=self)
        self.types = TypesAPI(self._config, api_version="playground", cognite_client=self)
