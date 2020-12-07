# Examples for the Integrations and Runs APIs
Create a client and try next possible operations
```python
from cognite.experimental import CogniteClient

client = CogniteClient(api_key="<<itera-int-green api key>>", project="itera-int-green", base_url = "https://greenfield.cognitedata.com")

# Create integration

from cognite.experimental.data_classes import Integration	
i1 = Integration(external_id = "py test id", name="py test", description = "python generated", data_set_id = 1, schedule = "", owner = {"name": "Alex", "email": "Alex@test.no"})
res = client.integrations.create(i1)

#Get list
integrations_list = client.integrations.list()

#Update existed integration
res.description = "New description"
res = client.integrations.update(res)

#or
from cognite.experimental.data_classes import IntegrationUpdate	
up = IntegrationUpdate(id=res.id)
up.description.set("Another new integration")
res = client.integrations.update(up)

#getById
res1 = client.integrations.retrieve(id=res.id)

#list of runs 
runsList = client.runs.list(external_id=res1.external_id)

#add new run with status
from cognite.experimental.data_classes import IntegrationRun	
newRun = client.runs.create(IntegrationRun(external_id=res1.external_id, status="success"))

#delete integration with all runs
client.integrations.delete(id=res1.id)
```

