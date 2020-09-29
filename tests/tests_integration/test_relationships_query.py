import uuid
from collections import namedtuple

import pytest

from cognite.client.beta import CogniteClient
from cognite.client.data_classes import (
    Asset,
    DataSet,
    Event,
    FileMetadata,
    Label,
    LabelDefinition,
    Relationship,
    Sequence,
    TimeSeries,
)
from cognite.experimental import RelationshipsQuery

COGNITE_CLIENT = CogniteClient()
API_REL = COGNITE_CLIENT.relationships
REL_QUERY_ENGINE = RelationshipsQuery(COGNITE_CLIENT)


@pytest.fixture
def new_assets():
    resources = [Asset(name="any", external_id=uuid.uuid4().hex[0:20]) for _ in range(2)]
    COGNITE_CLIENT.assets.create(resources)
    yield resources
    COGNITE_CLIENT.assets.delete(external_id=[res.external_id for res in resources])


@pytest.fixture
def new_time_series():
    resources = [TimeSeries(name="any", external_id=uuid.uuid4().hex[0:20]) for _ in range(2)]
    COGNITE_CLIENT.time_series.create(resources)
    yield resources
    COGNITE_CLIENT.time_series.delete(external_id=[res.external_id for res in resources])


@pytest.fixture
def new_files():
    resources = [FileMetadata(name="any", external_id=uuid.uuid4().hex[0:20]) for _ in range(2)]
    for res in resources:
        COGNITE_CLIENT.files.create(res)
    yield resources
    COGNITE_CLIENT.files.delete(external_id=[res.external_id for res in resources])


@pytest.fixture
def new_sequence():
    resources = [
        Sequence(name="any", columns=[{"external_id": "foo"}], external_id=uuid.uuid4().hex[0:20]) for _ in range(2)
    ]
    COGNITE_CLIENT.sequences.create(resources)
    yield resources
    COGNITE_CLIENT.sequences.delete(external_id=[res.external_id for res in resources])


@pytest.fixture
def new_events():
    resources = [Event(type="any", external_id=uuid.uuid4().hex[0:20]) for _ in range(2)]
    COGNITE_CLIENT.events.create(resources)
    yield resources
    COGNITE_CLIENT.events.delete(external_id=[res.external_id for res in resources])


@pytest.fixture
def new_label():
    external_id = uuid.uuid4().hex[0:20]
    tp = COGNITE_CLIENT.labels.create(LabelDefinition(external_id=external_id, name="mandatory"))
    assert isinstance(tp, LabelDefinition)
    yield tp
    COGNITE_CLIENT.labels.delete(external_id=tp.external_id)


@pytest.fixture
def new_data_set():
    external_id = uuid.uuid4().hex[0:20]
    d = COGNITE_CLIENT.data_sets.create(DataSet(external_id=external_id, name="relationships-query"))
    yield d.id
    # There are no delete endpoint for data sets


AllResources = namedtuple("AllResources", ["assets", "timeSeries", "events", "files", "sequences"])


@pytest.fixture
def new_relationships(new_label, new_data_set, new_assets, new_events, new_time_series, new_files, new_sequence):
    label_ext_id = new_label.external_id

    def gen_id():
        return uuid.uuid4().hex[0:20]

    def create_relationship(type, ext_id):
        return Relationship(
            external_id=gen_id(),
            source_type="asset",
            source_external_id=new_assets[0].external_id,
            target_type=type,
            target_external_id=ext_id,
            data_set_id=new_data_set,
            labels=[Label(label_ext_id)],
        )

    relationshipList = [create_relationship("asset", new_assets[1].external_id)]

    for res in new_events:
        relationshipList.append(create_relationship("event", res.external_id))

    for res in new_time_series:
        relationshipList.append(create_relationship("timeSeries", res.external_id))

    for res in new_files:
        relationshipList.append(create_relationship("file", res.external_id))

    for res in new_sequence:
        relationshipList.append(create_relationship("sequence", res.external_id))

    relationships = API_REL.create(relationshipList)
    yield relationships, new_data_set, AllResources(new_assets, new_time_series, new_events, new_files, new_sequence)
    API_REL.delete(external_id=[ext_ids["external_id"] for ext_ids in relationships.dump()])


class TestRelationshipsQuery:
    def test_all(self, new_relationships):
        _, data_set_id, resources = new_relationships
        data_set_id
        query_result = list(REL_QUERY_ENGINE.query(data_set_ids=[{"id": data_set_id}]))
        assert len(query_result) > 0
        for rel in query_result:
            assert rel.source_resource.external_id == resources.assets[0].external_id
            if rel.relationship.target_type == "timeSeries":
                assert rel.target_resource.external_id in [res.external_id for res in resources.timeSeries]
            if rel.relationship.target_type == "event":
                assert rel.target_resource.external_id in [res.external_id for res in resources.events]
            if rel.relationship.target_type == "file":
                assert rel.target_resource.external_id in [res.external_id for res in resources.files]
            if rel.relationship.target_type == "sequence":
                assert rel.target_resource.external_id in [res.external_id for res in resources.sequences]
