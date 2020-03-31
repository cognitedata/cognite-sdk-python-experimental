
# Examples for the Contextualization API
## Entity matcher
```python
from cognite.experimental import CogniteClient

client = CogniteClient(client_name="datastudio")

training_data = ["21PT1019", "13FV1234", "84PAH93234"]
model = await client.entity_matching.fit(training_data)

predict_data = ["IAA_21PT1019.PV", "IAA_13FV1234.PV", "IAA_84PAH93234.PV"]
job = await model.predict(predict_data)
matches = job.items
print(matches)
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
rules_job = await client.entity_matching.create_rules(matches)
rules_job.items
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
job = await client.pnid_parsing.parse(file_id=1234,entities=['string1','string2'])
svg_url = job.svg_url
```

## Resource typing
```python
training_data = [
  {
    "data": ["05-V-0363", "ISOLATION VALVE Y4-PSH-025"],
    "target": "valve"
  },
  {
    "data": ["65-V-5284", "BLOCK VALVE FOR STBD MAIN HYDRAULIC PRESSURE SUPPLY TO PORT MAIN HYDRAULIC PRESSURE LINE"],
    "target": "valve"
  },
  {
    "data": ["0300A-WF-71-L-0837-AD75-04","71-L-0837"],
    "target": "pipe"
  },
  {
    "data": ["0150J-PL-39-L-5064-TC02-00","39-L-5064"],
    "target": "pipe"
  }
]
model = await client.entity_matching.fit(training_data)

predict_data = [{
    "data": ["0600-DO-81L5090-AC21", "FROM DRAIN GULLY"]
  }, {
    "data": ["65-GC-12002", "FILTER"]
  }, {
    "data": ["48-SX-9225-J01", "SAFETY, ESCAPE AND FIREFIGHTING, JUNCTION BOX"]
  }]
matches = await model.predict(predict_data)
print(matches.items)
```
will produce the following output after a few seconds:
```python
{
  'items': [
    {
      'input': ['0600-DO-81L5090-AC21', 'FROM DRAIN GULLY'],
      'target': 'valve'
    }, {
      'input': ['65-GC-12002', 'FILTER'],
      'target': 'other'
    }, {
      'input': ['48-SX-9225-J01', 'SAFETY, ESCAPE AND FIREFIGHTING, JUNCTION BOX'],
      'target': 'other'
    }
  ]
}
```


## Entity Extraction

The following methods are available for a project whitelisted for unstructured search, and only for file types supported in the search index. 
```python
job = await client.entity_extraction.extract(entities=["23-VG-9102", "23-VG-1000-not-existing"], 
                               file_ids = [6240763514226915])
print(job.items)
```

will produce an output similar to:
```python
[{'fileId': 6240763514226915, 'entities': ['23-VG-9102']}]
```
