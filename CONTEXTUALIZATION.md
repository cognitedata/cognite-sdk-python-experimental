
# Examples for the Contextualization API
Create a client
```python
from cognite.experimental import CogniteClient

client = CogniteClient(client_name="cognite-sdk-python-experimental")
```

## Entity Matcher

### Fit a supervised Entity Matching Model
Fit a model
```python
match_from = [
    {"id":0, "name" : "IAA_21PT1019.PV", "description": "correct"}, 
    {"id":1, "name" : "IAA_13FV1234.PV", "description": "ok"}
]
match_to = [
    {"id":0, "name" : "21PT1019", "description": "correct"}, 
    {"id":1, "name" : "21PT1019", "description": "wrong"}, 
    {"id":2, "name" : "13FV1234", "description": "not ok"},
    {"id":3, "name" : "13FV1234", "description": "ok"},
    {"id":4, "name" : "84PAH93234", "description": "some description"},
    {"id":5, "name" : "84PAH93234", "description": ""},
]
true_matches = [(0,0)]

model = client.entity_matching.fit(match_from = match_from,
                                      match_to = match_to,
                                      true_matches = true_matches,
                                      match_fields = [("name", "name"), ("description", "description")]
)
```
#### Refit model with additional true match pair
```python
true_matches = [(1,3)]

model = model.refit(true_matches = true_matches)
```

#### Predict on the training data
```python
job = model.predict(num_matches = 2)
matches = job.result
print(matches["items"])
```
will produce the following output after a few seconds:
```python
[
  {
    'matchFrom': {'description': 'correct', 'id': 0, 'name': 'IAA_21PT1019.PV'},
    'matches': [
      {'matchTo': {'description': 'correct', 'id': 0,'name': '21PT1019'}, 'score': 0.9},
      {'matchTo': {'description': 'wrong', 'id': 1, 'name': '21PT1019'}, 'score': 0.0}
    ]
  },
 {
   'matchFrom': {'description': 'ok', 'id': 1, 'name': 'IAA_13FV1234.PV'},
   'matches': [
      {'matchTo': {'description': 'ok', 'id': 3, 'name': '13FV1234'}, 'score': 0.9},
      {'matchTo': {'description': 'not ok', 'id': 2, 'name': '13FV1234'}, 'score': 0.2}
    ]
  }
]
```
#### Predict on new data
```python
match_from = [
    {"id":2, "name" : "IAA_84PAH93234.PV", "description": "some description"},
]
job = model.predict(num_matches = 2, match_from = match_from)
matches = job.result
print(matches["items"])
```
will produce the following output after a few seconds:
```python
[
  {
    'matchFrom': {'description': 'some description', 'id': 2, 'name': 'IAA_84PAH93234.PV'}, 
    'matches': [
      {'matchTo': {'description': 'some description', 'id': 4, 'name': '84PAH93234'}, 'score': 0.9}, 
      {'matchTo': {'description': '', 'id': 5, 'name': '84PAH93234'}, 'score': 0.0}
    ]
  }
]
```

### Fit an unsupervised Entity Matching Model
Fit a model
```python
match_from = [
    {"id":0, "name" : "IAA_21PT1019.PV", "description": "correct"}, 
    {"id":1, "name" : "IAA_13FV1234.PV", "description": "ok"}
]
match_to = [
    {"id":0, "name" : "21PT1019", "description": "correct"}, 
    {"id":1, "name" : "21PT1019", "description": "wrong"}, 
    {"id":2, "name" : "13FV1234", "description": "not ok"},
    {"id":3, "name" : "13FV1234", "description": "ok"},
    {"id":4, "name" : "84PAH93234", "description": "some description"},
    {"id":5, "name" : "84PAH93234", "description": ""},
]

model = client.entity_matching.fit(match_from = match_from,
                                      match_to = match_to,
                                      match_fields = [("name", "name"), ("description", "description")]
)
```
#### Predict on the training data
```python
job = model.predict(num_matches = 2)
matches = job.result
print(matches["items"])
```
will produce the following output after a few seconds:
```python
[
  {
    'matchFrom': {'description': 'correct', 'id': 0, 'name': 'IAA_21PT1019.PV'},
    'matches': [
      {'matchTo': {'description': 'correct', 'id': 0,'name': '21PT1019'}, 'score': 1.0},
      {'matchTo': {'description': 'wrong', 'id': 1, 'name': '21PT1019'}, 'score': 0.5000000000000001}
    ]
  },
  {
    'matchFrom': {'description': 'ok', 'id': 1, 'name': 'IAA_13FV1234.PV'},
    'matches': [
      {'matchTo': {'description': 'ok', 'id': 3, 'name': '13FV1234'}, 'score': 1.0},
      {'matchTo': {'description': 'not ok', 'id': 2, 'name': '13FV1234'}, 'score': 0.8535533905932738}
    ]
  }
]
```

You can also call predict by external_id or id directly.
```python
job = client.entity_matching.predict(num_matches = 2,external_id="my_model")
job = client.entity_matching.predict(num_matches = 2,id=1234)
```

### Create Rules

```python
matches = [
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

```python
rules_job = client.entity_matching.create_rules(matches)
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

## P&ID Parser
When the file_id is a valid file_id from the project associated with the client, this will print the url for the svg as a string after a few seconds.
```python
job = client.pnid_parsing.parse(file_id=1234,entities=['string1','string2'])
svg_url = job.result['svgUrl']
```

## Entity Extraction

The following methods are available for a project whitelisted for unstructured search, and only for file types supported in the search index. 
```python
job = client.entity_extraction.extract(entities=["23-VG-9102", "23-VG-1000-not-existing"], 
                               file_ids = [1234])
print(job.result['items'])
```

When the file_id is a valid file_id from the project associated with the client, will produce the following output:
```python
[{'fileId': 1234, 'entities': ['23-VG-9102']}]
```
