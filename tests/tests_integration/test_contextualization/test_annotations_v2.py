from copy import deepcopy
from email.mime import base
from typing import List, Optional

import pytest
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import AnnotationV2, AnnotationV2Filter, AnnotationV2List, AnnotationV2Update

COGNITE_CLIENT = CogniteClient()
ANNOTATIONSAPI = COGNITE_CLIENT.annotations_v2


def delete_with_check(delete_ids: List[int], check_ids: Optional[List[int]] = None) -> None:
    if check_ids is None:
        check_ids = delete_ids
    ANNOTATIONSAPI.delete(id=delete_ids)
    try:
        ANNOTATIONSAPI.retrieve_multiple(check_ids)
        raise ValueError(f"retrieve_multiple successful for ids {check_ids}")
    except CogniteAPIError as e:
        assert "Some annotation(s) not found" in str(e)
        assert e.code == 404
        missing = [i["id"] for i in e.missing]
        assert sorted(check_ids) == sorted(missing)


def cleanup(check_ids: List[int] = []) -> None:
    """ Cleanup all annotations with creating_app=='UnitTest' """
    file_ids = [f.id for f in COGNITE_CLIENT.files.list(limit=100) if f.id]
    filter = AnnotationV2Filter(
        annotated_resource_type="file",
        annotated_resource_ids=[{"id": fid} for fid in file_ids],
        creating_app="UnitTest",
    )
    annotation_ids = [a.id for a in ANNOTATIONSAPI.list(filter=filter)]
    delete_with_check(annotation_ids, check_ids)


@pytest.fixture
def file_id() -> int:
    files = COGNITE_CLIENT.files.list(limit=100)
    for file in files:
        if file.id:
            return file.id
    raise ValueError("No file found")


@pytest.fixture
def base_annotation(annotation: AnnotationV2, file_id: int):
    base_annotation = deepcopy(annotation)
    base_annotation.annotated_resource_id = file_id
    return base_annotation


@pytest.fixture
def new_annotation(base_annotation: AnnotationV2) -> AnnotationV2:
    created_annotation = ANNOTATIONSAPI.create(base_annotation)
    yield created_annotation
    cleanup([created_annotation.id])


@pytest.fixture
def new_annotations(base_annotation: AnnotationV2) -> AnnotationV2List:
    created_annotations = ANNOTATIONSAPI.create([base_annotation] * 10)
    yield created_annotations
    cleanup([a.id for a in created_annotations])


def check_created_vs_base(base_annotation: AnnotationV2, created_annotation: AnnotationV2) -> None:
    base_dump = base_annotation.dump()
    created_dump = created_annotation.dump()
    found_special_keys = 0
    for k, v in created_dump.items():
        if k in ["id", "created_time", "last_updated_time"]:
            found_special_keys += 1
            assert v is not None
        else:
            assert v == base_dump[k]
    assert found_special_keys == 3


class TestAnnotationsV2Integration:
    def test_create_single_annotation(self, base_annotation: AnnotationV2, new_annotation: AnnotationV2) -> None:
        assert isinstance(new_annotation, AnnotationV2)
        check_created_vs_base(base_annotation, new_annotation)

    def test_create_annotations(self, base_annotation: AnnotationV2, new_annotations) -> None:
        assert isinstance(new_annotations, AnnotationV2List)
        for a in new_annotations:
            check_created_vs_base(base_annotation, a)

    def test_delete_annotations(self, new_annotations: AnnotationV2List) -> None:
        delete_with_check([a.id for a in new_annotations])

    def test_update_annotation_by_annotation(self, new_annotation: AnnotationV2) -> None:
        new_annotation.linked_resource_type = "asset"
        new_annotation.linked_resource_id = 1
        updated = ANNOTATIONSAPI.update(new_annotation)
        assert isinstance(updated, AnnotationV2)
        updated_dump = updated.dump()
        new_annotation_dump = new_annotation.dump()
        for k, v in updated_dump.items():
            if k == "last_updated_time":
                assert v > new_annotation_dump[k]
            else:
                assert v == new_annotation_dump[k]

    def test_update_annotation_by_annotation_update(self, new_annotation: AnnotationV2) -> None:
        update = {
            "data": {
                "pageNumber": 1,
                "assetRef": {"id": 1, "externalId": None},
                "textRegion": {"xMin": 0.5, "xMax": 1.0, "yMin": 0.5, "yMax": 1.0},
                "symbolRegion": {"xMin": 0.0, "xMax": 0.5, "yMin": 0.5, "yMax": 1.0},
            },
            "status": "rejected",
            "annotation_type": "diagrams.AssetLink",
            "linked_resource_type": "asset",
            "linked_resource_id": 1,
            "linked_resource_external_id": None,
        }
        annotation_update = AnnotationV2Update(id=new_annotation.id)
        for k, v in update.items():
            getattr(annotation_update, k).set(v)

        updated = ANNOTATIONSAPI.update([annotation_update])
        assert isinstance(updated, AnnotationV2List)
        updated = updated[0]
        for k, v in update.items():
            assert getattr(updated, k) == v

    def test_list(self, annotation: AnnotationV2, new_annotations: AnnotationV2List) -> None:
        file_id = new_annotations[0].annotated_resource_id
        annotation = deepcopy(annotation)
        annotation.annotated_resource_id = file_id
        filter = AnnotationV2Filter(
            annotated_resource_type=annotation.annotated_resource_type,
            annotated_resource_ids=[{"id": file_id}],
            status=annotation.status,
            creating_app=annotation.creating_app,
            creating_app_version=annotation.creating_app_version,
            creating_user=annotation.creating_user,
        )
        annotations_list = ANNOTATIONSAPI.list(filter=filter)
        assert isinstance(annotations_list, AnnotationV2List)
        assert len(annotations_list) == len(new_annotations)
        for attr in [
            "annotated_resource_type",
            "annotated_resource_id",
            "status",
            "creating_app",
            "creating_app_version",
            "creating_user",
        ]:
            for a in annotations_list:
                assert getattr(a, attr) == getattr(annotation, attr)

    def test_retrieve(self, new_annotation: AnnotationV2) -> None:
        retrieved_annotation = ANNOTATIONSAPI.retrieve(new_annotation.id)
        assert isinstance(retrieved_annotation, AnnotationV2)
        assert new_annotation.dump() == retrieved_annotation.dump()

    def test_retrieve_multiple(self, new_annotations: AnnotationV2List) -> None:
        ids = [c.id for c in new_annotations]
        retrieved_annotations = ANNOTATIONSAPI.retrieve_multiple(ids)
        assert isinstance(retrieved_annotations, AnnotationV2List)
        for ret, new in zip(retrieved_annotations, new_annotations):
            assert ret.dump() == new.dump()
