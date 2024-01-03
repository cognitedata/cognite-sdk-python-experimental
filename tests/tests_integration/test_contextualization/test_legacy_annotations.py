import pytest

from cognite.client.exceptions import CogniteAPIError
from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    LegacyAnnotation,
    LegacyAnnotationFilter,
    LegacyAnnotationList,
    LegacyAnnotationUpdate,
)

COGNITE_CLIENT = CogniteClient()
ANNOTATIONSAPI = COGNITE_CLIENT.legacy_annotations


@pytest.fixture
def new_annotation():
    event = COGNITE_CLIENT.events.list(limit=1)[0]
    annot = LegacyAnnotation(
        annotation_type="abc",
        annotated_resource_id=event.id,
        annotated_resource_type="event",
        source="sdk-integration-tests",
    )

    c_annot = ANNOTATIONSAPI.create(annot)
    yield c_annot
    ANNOTATIONSAPI.delete(id=c_annot.id)
    try:
        ANNOTATIONSAPI.retrieve(c_annot.id)
    except CogniteAPIError as e:
        assert "Could not find" in str(e)


@pytest.fixture
def new_annotations():
    asset = next(a for a in COGNITE_CLIENT.assets.list(limit=100) if a.external_id)
    annot = LegacyAnnotation(
        annotation_type="abc",
        annotated_resource_id=asset.id,
        annotated_resource_type="asset",
        source="sdk-integration-tests",
    )
    annots = [annot] * 10

    c_annots = ANNOTATIONSAPI.create(annots)
    c_ids = [c.id for c in c_annots]
    yield c_annots
    ANNOTATIONSAPI.delete(id=c_ids)
    for id in c_ids:
        try:
            ANNOTATIONSAPI.retrieve(id)
        except CogniteAPIError as e:
            assert "Could not find" in str(e)


class TestAnnotationsIntegration:
    def test_create_single_annotation(self, new_annotation):
        assert isinstance(new_annotation, LegacyAnnotation)

    def test_create_annotations(self, new_annotations):
        assert isinstance(new_annotations, LegacyAnnotationList)

    def test_update_annotations(self, new_annotation):
        new_annotation.text = "new_text"
        updated = ANNOTATIONSAPI.update(new_annotation)
        assert isinstance(updated, LegacyAnnotation)
        assert new_annotation.text == updated.text
        updated_patch = ANNOTATIONSAPI.update(
            [
                LegacyAnnotationUpdate(id=new_annotation.id)
                .data.set({"foo": "bar"})
                .text.set("text")
                .status.set("status")
                .region.set({"re": "gion"})
            ]
        )
        assert isinstance(updated_patch, LegacyAnnotationList)
        assert {"foo": "bar"} == updated_patch[0].data
        assert "text" == updated_patch[0].text
        assert "status" == updated_patch[0].status
        assert {"re": "gion"} == updated_patch[0].region

    def test_list(self, new_annotations):
        assert isinstance(new_annotations, LegacyAnnotationList)

        fil = LegacyAnnotationFilter(annotation_type="abc", annotated_resource_type="asset")
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, LegacyAnnotationList)
        assert all([l_annot.annotation_type == "abc" for l_annot in l_annots])

        fil = {"annotation_type": "abc", "annotatedResourceType": "asset"}
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, LegacyAnnotationList)
        assert all([l_annot.annotation_type == "abc" for l_annot in l_annots])

        fil = LegacyAnnotationFilter(
            annotated_resource_ids=[{"id": new_annotations[0].annotated_resource_id}],
            annotated_resource_type="asset",
        )
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, LegacyAnnotationList)
        assert all([l_annot.annotated_resource_id == new_annotations[0].annotated_resource_id for l_annot in l_annots])

        fil = LegacyAnnotationFilter(
            annotated_resource_ids=[{"id": new_annotations[0].annotated_resource_id}],
            annotated_resource_type="asset",
        )
        l_annots = ANNOTATIONSAPI.list(limit=5, filter=fil)
        assert isinstance(l_annots, LegacyAnnotationList)
        assert len(l_annots) == 5
        assert all([l_annot.annotated_resource_id == new_annotations[0].annotated_resource_id for l_annot in l_annots])

    def test_retrieve_multiple(self, new_annotations):
        assert isinstance(new_annotations, LegacyAnnotationList)

        r_annot = ANNOTATIONSAPI.retrieve(new_annotations[0].id)
        assert isinstance(r_annot, LegacyAnnotation)
        assert r_annot.id == new_annotations[0].id

        c_ids = [c.id for c in new_annotations]
        r_annots = ANNOTATIONSAPI.retrieve_multiple(c_ids)
        assert isinstance(r_annots, LegacyAnnotationList)
        assert len(r_annots) == 10
        assert all([r.id in c_ids for r in r_annots])
