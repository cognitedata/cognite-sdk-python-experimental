
# Examples for the Contextualization API
## Entity matcher
```python
from cognite.experimental import CogniteClient

client = CogniteClient(client_name="datastudio")

training_data = ["21PT1019", "13FV1234", "84PAH93234"]
model = client.entity_matching.fit(training_data)

predict_data = ["IAA_21PT1019.PV", "IAA_13FV1234.PV", "IAA_84PAH93234.PV"]
job = model.predict(predict_data) # at this point the client waits for model fit completion
matches = job.result # at this point the client waits for job completion
print(matches['items'])
```
will produce the following output after a few seconds: 
```python
[
    {
      'input': 'IAA_21PT1019.PV',
      'predicted': '21PT1019',
      'score': 0.999998845300462
    }, {
      'input': 'IAA_13FV1234.PV',
      'predicted': '13FV1234',
      'score': 0.999998845300462
    }, {
      'input': 'IAA_84PAH93234.PV',
      'predicted': '84PAH93234',
      'score': 0.999998845300462
    }
]

```

### Create rules
After first running the entity matcher
```python
rules_job = client.entity_matching.create_rules(matches["items"])
rules_job.result
```
will produce the following output after a few seconds:
```python
[
    {
      'avgScore': 0.999998845300462,
      'inputPattern': '[D2][L3][D1]',
      'matchIndex': [0, 1],
      'numMatches': 2,
      'predictPattern': 'L_[D2][L3][D1].L'
    }, {
      'avgScore': 0.999998845300462,
      'inputPattern': '[D1][L3][D2]',
      'matchIndex': [2],
      'numMatches': 1,
      'predictPattern': 'L_[D1][L3][D2].L'
    }
]

```
## P&ID parser
This will print the url for the svg as a string after a few seconds.
```python
job = client.pnid_parsing.parse(file_id=1234,entities=['string1','string2'])
svg_url = job.result['svgUrl']
```

## Entity Extraction

The following methods are available for a project whitelisted for unstructured search, and only for file types supported in the search index. 
```python
job = client.entity_extraction.extract(entities=["23-VG-9102", "23-VG-1000-not-existing"], 
                               file_ids = [6240763514226915])
print(job.result['items'])
```

will produce an output similar to:
```python
[{'fileId': 6240763514226915, 'entities': ['23-VG-9102']}]
```
