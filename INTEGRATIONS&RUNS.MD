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
i1 = Integration(external_id = "py test id", name="py test", description = "python generated", data_set_id = 1, schedule = "", owner = {"name": "Alex", "email": "Alex@test.no"})
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
res = client.integrations.update(up)
```

##Retrieve an integration by id
```python
res1 = client.integrations.retrieve(id=res.id)
```

##List integration runs 
```python
runsList = client.runs.list(external_id=res1.external_id)
```

##Create a new integration run with status
```python
from cognite.experimental.data_classes import IntegrationRun	
newRun = client.runs.create(IntegrationRun(external_id=res1.external_id, status="success"))
```

##Delete an integration and all its runs
```python
client.integrations.delete(id=res1.id)
```
