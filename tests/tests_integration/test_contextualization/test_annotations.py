import pytest
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Annotation, AnnotationFilter, AnnotationList, ContextualizationJob

COGNITE_CLIENT = CogniteClient(debug=True)
ANNOTATIONSAPI = COGNITE_CLIENT.annotations


@pytest.fixture
def new_annotation():
    annot = Annotation(
        annotation_type="abc",
        annotated_resource_external_id="foo",
        annotated_resource_type="bar",
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
    annot = Annotation(
        annotation_type="abc",
        annotated_resource_external_id="foo",
        annotated_resource_type="bar",
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
        assert isinstance(new_annotation, Annotation)

    def test_create_annotations(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

    def test_list_annotation_type(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

        fil = AnnotationFilter(annotation_type="abc")
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert all([l.annotation_type == "abc" for l in l_annots])

    def test_list_annotation_type_dict_filter(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

        fil = {"annotation_type": "abc"}
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert all([l.annotation_type == "abc" for l in l_annots])

    def test_list_annotation_type_no_filter(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)
        l_annots = ANNOTATIONSAPI.list()
        assert isinstance(l_annots, AnnotationList)

    def test_list_annotated_resource_external_id(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

        fil = AnnotationFilter(annotated_resource_ids=[{"external_id": "foo"}])
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert all([l.annotated_resource_external_id == "foo" for l in l_annots])

    def test_list_limit_with_annotated_resource_external_id(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

        fil = AnnotationFilter(annotated_resource_ids=[{"external_id": "foo"}])
        l_annots = ANNOTATIONSAPI.list(limit=5, filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert len(l_annots) == 5
        assert all([l.annotated_resource_external_id == "foo" for l in l_annots])

    def test_retrieve_multiple(self, new_annotations):
        assert isinstance(new_annotations, AnnotationList)

        c_ids = [c.id for c in new_annotations]
        r_annots = ANNOTATIONSAPI.retrieve_multiple(c_ids)
        assert isinstance(r_annots, AnnotationList)
        assert len(r_annots) == 10
        assert all([r.id in c_ids for r in r_annots])

    def test_retrieve(self, new_annotation):
        assert isinstance(new_annotation, Annotation)
        r_annot = ANNOTATIONSAPI.retrieve(new_annotation.id)
        assert isinstance(r_annot, Annotation)
        assert r_annot.id == new_annotation.id
