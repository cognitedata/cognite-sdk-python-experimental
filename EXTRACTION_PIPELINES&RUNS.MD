# Examples for the ExtractionPipelines and Runs APIs
## Create a client
```python
from cognite.experimental import CogniteClient

client = CogniteClient(api_key="<>", project="your project")
```
API key must have read/write permissions for the IntegrationsAcl or DatasetsAcl.
You need to create a group that has Acl support
```json
{"items": [{"name": "datasets-readwrite", "capabilities": [{"datasetsAcl": {"actions": ["READ", "WRITE"], "scope": {"all": {}}}}]}]}
``` 
Then add users that should have access to ExtractionPipelines to that 'datasets-readwrite' group


## Create an ExtractionPipeline

```python
from cognite.experimental.data_classes import ExtractionPipeline

ep1 = ExtractionPipeline(external_id="py test id", name="py test", description="python generated", data_set_id=1,
                         schedule="", contacts=[{"name": "Name", "email": "Name@test.no", "sendNotification": True}])
res = client.extraction_pipelines.create(ep1)
```

## List ExtractionPipelines
```python
ext_pipes_list = client.extraction_pipelines.list()
list2 = client.extraction_pipelines.list(limit=6)
list3 = client.extraction_pipelines.list(name="Name")
list4 = client.extraction_pipelines.list(external_id_prefix="FX")
contacts=[{"name": "Name", "email": "Name@test.no", "sendNotification": True}]
list5 = client.extraction_pipelines.list(contacts=contacts)
list6 = client.extraction_pipelines.list(data_set_ids=[11111111, 22222])
list7 = client.extraction_pipelines.list(data_set_external_ids=["ext1", "ext2"])
```

##Update an ExtractionPipeline that already exists
```python
res.description = "New description"
res = client.extraction_pipelines.update(res)

#or
from cognite.experimental.data_classes import ExtractionPipelineUpdate	
up = ExtractionPipelineUpdate(id=res.id)
up.description.set("Another new entity")
up.raw_tables.add([{"dbName": "name", "tableName": "name"}])
up.raw_tables.remove([{"dbName": "old_name", "tableName": "old_name"}])
res = client.extraction_pipelines.update(up)
```

##Retrieve an ExtractionPipeline by id
```python
res1 = client.extraction_pipelines.retrieve(id=res.id)
```

##Retrieve ExtractionPipelines by ids and external ids
```python
epList = client.extraction_pipelines.retrieve_multiple(ids=[23, 24, 25, 120], external_ids=['test_id'])
```

##List Events for given ExtractionPipeline by ExtractionPipeline id
```python
res = client.extraction_pipelines.list_events(ext_pipe_id=675)
```

##Get Event by its id and referred ExtractionPipeline id
```python
res = client.extraction_pipelines.get_event(ext_pipe_id=675, event_id=112)
```

##List ExtractionPipeline runs 
```python
runsList = client.extraction_pipeline_runs.list(external_id=res1.external_id)
```

##Filter ExtractionPipeline runs 
```python
runsList = client.extraction_pipeline_runs.list(external_id=res1.external_id, statuses=['success'])
```

##Create a new ExtractionPipeline run with status
```python
from cognite.experimental.data_classes import ExtractionPipelineRun	
newRun = client.extraction_pipeline_runs.create(ExtractionPipelineRun(external_id=res1.external_id, status="success"))
newFailureRun = client.extraction_pipeline_runs.create(ExtractionPipelineRun(external_id=res1.external_id, status="failure", message="Error message"))
```

##Delete an ExtractionPipeline and all its runs
```python
client.extraction_pipelines.delete(id=res1.id)
```
