import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Annotation, AnnotationFilter, AnnotationList, ContextualizationJob

COGNITE_CLIENT = CogniteClient(debug=True)
ANNOTATIONSAPI = COGNITE_CLIENT.annotations


class TestAnnotationsIntegration:
    def test_create_single_annotation(self):
        annot = Annotation(
            annotation_type="abc",
            annotated_resource_external_id="foo",
            annotated_resource_type="file",
            source="sdk-integration-tests",
        )
        c_annot = ANNOTATIONSAPI.create(annot)
        assert isinstance(c_annot, Annotation)
        ANNOTATIONSAPI.delete(id=c_annot.id)

    def test_create_annotations(self):
        annots = []
        for i in range(3):
            annot = Annotation(
                annotation_type="abc",
                annotated_resource_external_id="foo" + str(i),
                annotated_resource_type="file",
                source="sdk-integration-tests",
            )
            annots.append(annot)

        c_annots = ANNOTATIONSAPI.create(annots)
        assert isinstance(c_annots, AnnotationList)
        ANNOTATIONSAPI.delete(id=[c.id for c in c_annots])

    def test_list_annotation_type(self):
        annots = []
        for _ in range(3):
            annot = Annotation(
                annotation_type="abc",
                annotated_resource_external_id="foo",
                annotated_resource_type="file",
                source="sdk-integration-tests",
            )
            annots.append(annot)

        c_annots = ANNOTATIONSAPI.create(annots)

        fil = AnnotationFilter(annotation_type="abc")
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert all([l.annotation_type == "abc" for l in l_annots])

        ANNOTATIONSAPI.delete(id=[c.id for c in c_annots])

    def test_list_annotated_resource_external_id(self):
        annots = []
        for _ in range(3):
            annot = Annotation(
                annotation_type="abc",
                annotated_resource_external_id="bar",
                annotated_resource_type="file",
                source="sdk-integration-tests",
            )
            annots.append(annot)

        c_annots = ANNOTATIONSAPI.create(annots)

        fil = AnnotationFilter(annotated_resource_ids=[{"external_id": "bar"}])
        l_annots = ANNOTATIONSAPI.list(filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert all([l.annotated_resource_external_id == "bar" for l in l_annots])
        ANNOTATIONSAPI.delete(id=[c.id for c in c_annots])

    def test_list_limit_with_annotated_resource_external_id(self):
        annots = []
        for _ in range(10):
            annot = Annotation(
                annotation_type="abc",
                annotated_resource_external_id="foobar",
                annotated_resource_type="file",
                source="sdk-integration-tests",
            )
            annots.append(annot)

        c_annots = ANNOTATIONSAPI.create(annots)

        fil = AnnotationFilter(annotated_resource_ids=[{"external_id": "foobar"}])
        l_annots = ANNOTATIONSAPI.list(limit=5, filter=fil)
        assert isinstance(l_annots, AnnotationList)
        assert len(l_annots) == 5
        assert all([l.annotated_resource_external_id == "foobar" for l in l_annots])
        ANNOTATIONSAPI.delete(id=[c.id for c in c_annots])

    def test_retrieve(self):
        annots = []
        for _ in range(10):
            annot = Annotation(
                annotation_type="abc",
                annotated_resource_external_id="retfoo",
                annotated_resource_type="file",
                source="sdk-integration-tests",
            )
            annots.append(annot)
        c_annots = ANNOTATIONSAPI.create(annots)
        c_ids = [annot.id for annot in c_annots]

        r_annots = ANNOTATIONSAPI.retrieve(c_ids)

        assert isinstance(r_annots, AnnotationList)
        assert len(r_annots) == 10
        assert all([r.id in c_ids for r in r_annots])

        ANNOTATIONSAPI.delete(id=[c.id for c in c_annots])
