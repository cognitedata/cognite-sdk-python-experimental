import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import Annotation, ContextualizationJob

COGNITE_CLIENT = CogniteClient(debug=True)
ANNOTATIONSAPI = COGNITE_CLIENT.annotations


class TestAnnotationsIntegration:
    def test_create_delete(self):
        annot = Annotation(
            annotation_type="abc",
            annotated_resource_external_id="foo",
            annotated_resource_type="file",
            source="sdk-integration-tests",
        )
        c_annot = ANNOTATIONSAPI.create(annot)
        ANNOTATIONSAPI.delete(id=c_annot.id)
