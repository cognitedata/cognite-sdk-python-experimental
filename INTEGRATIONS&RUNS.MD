# Examples for the Integrations and Runs APIs
## Create a client
```python
from cognite.experimental import CogniteClient

client = CogniteClient(api_key="<>", project="your project")
```
API key must have read/write permissions for the GenericAcl.
You need to create a group that has GenericAcl support
```json
{"items": [{"name": "generic-readwrite", "capabilities": [{"genericsAcl": {"actions": ["READ", "WRITE"], "scope": {"all": {}}}}]}]}
``` 
Then add users that should have access to integrations to that 'generic-readwrite' group


## Create an integration
```python
from cognite.experimental.data_classes import Integration	
i1 = Integration(external_id = "py test id", name="py test", description = "python generated", data_set_id = 1, schedule = "", contacts = [{"name": "Alex", "email": "Alex@test.no", "sendNotification": True}])
res = client.integrations.create(i1)
```

## List integrations
```python
integrations_list = client.integrations.list()
```

##Update an integration that already exists
```python
res.description = "New description"
res = client.integrations.update(res)

#or
from cognite.experimental.data_classes import IntegrationUpdate	
up = IntegrationUpdate(id=res.id)
up.description.set("Another new integration")
up.raw_tables.add([{"dbName": "name", "tableName": "name"}])
up.raw_tables.remove([{"dbName": "old_name", "tableName": "old_name"}])
res = client.integrations.update(up)
```

##Retrieve an integration by id
```python
res1 = client.integrations.retrieve(id=res.id)
```

##Retrieve integrations by ids and external ids
```python
intList = client.integrations.retrieve_multiple(ids=[23,24,25, 120], external_ids=['test_id'])
```

##List integration runs 
```python
runsList = client.integration_runs.list(external_id=res1.external_id)
```

##Create a new integration run with status
```python
from cognite.experimental.data_classes import IntegrationRun	
newRun = client.integration_runs.create(IntegrationRun(external_id=res1.external_id, status="success"))
newFailureRun = client.integration_runs.create(IntegrationRun(external_id=res1.external_id, status="failure", message = "Error message"))
```

##Delete an integration and all its runs
```python
client.integrations.delete(id=res1.id)
```
