from copy import deepcopy
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
        raise ValueError(f"retrieve_multiple after delete successful for ids {check_ids}")
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
    if annotation_ids:
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
def base_annotation2(base_annotation: AnnotationV2):
    base_annotation2 = deepcopy(base_annotation)
    base_annotation2.status = "rejected"
    return base_annotation2


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


def _test_list_on_created_annotations(annotations: AnnotationV2List, limit: int = 25):
    annotation = annotations[0]
    filter = AnnotationV2Filter(
        annotated_resource_type=annotation.annotated_resource_type,
        annotated_resource_ids=[{"id": annotation.annotated_resource_id}],
        status=annotation.status,
        creating_app=annotation.creating_app,
        creating_app_version=annotation.creating_app_version,
        creating_user=annotation.creating_user,
    )
    annotations_list = ANNOTATIONSAPI.list(filter=filter, limit=limit)
    assert isinstance(annotations_list, AnnotationV2List)
    if limit == -1 or limit > len(annotations):
        assert len(annotations_list) == len(annotations)
    else:
        assert len(annotations_list) == limit

    # TODO can use check_created_vs_base here?
    for attr in [
        "annotated_resource_type",
        "annotated_resource_id",
        "status",
        "creating_app",
        "creating_app_version",
        "creating_user",
    ]:
        base_attr = getattr(annotation, attr)
        for a in annotations_list:
            assert getattr(a, attr) == base_attr


class TestAnnotationsV2Integration:
    def test_create_single_annotation(self, base_annotation: AnnotationV2) -> None:
        created_annotation = ANNOTATIONSAPI.create(base_annotation)
        try:
            assert isinstance(created_annotation, AnnotationV2)
            check_created_vs_base(base_annotation, created_annotation)
        finally:
            delete_with_check([created_annotation.id])

    def test_create_annotations(self, base_annotation: AnnotationV2) -> None:
        created_annotations = ANNOTATIONSAPI.create([base_annotation] * 30)
        try:
            assert isinstance(created_annotations, AnnotationV2List)
            for a in created_annotations:
                check_created_vs_base(base_annotation, a)
        finally:
            delete_with_check([a.id for a in created_annotations])

    def test_delete_annotations(self, base_annotation: AnnotationV2) -> None:
        created_annotations = ANNOTATIONSAPI.create([base_annotation] * 30)
        delete_with_check([a.id for a in created_annotations])

    def test_update_annotation_by_annotation(self, base_annotation: AnnotationV2) -> None:
        created_annotation = ANNOTATIONSAPI.create(base_annotation)
        try:
            updated = deepcopy(created_annotation)
            updated.linked_resource_type = "asset"
            updated.linked_resource_id = 1
            updated = ANNOTATIONSAPI.update(created_annotation)
            assert isinstance(updated, AnnotationV2)
            updated_dump = updated.dump()
            created_annotation_dump = created_annotation.dump()
            for k, v in updated_dump.items():
                if k == "last_updated_time":
                    assert v > created_annotation_dump[k]
                else:
                    assert v == created_annotation_dump[k]
        finally:
            delete_with_check([created_annotation.id])

    def test_update_annotation_by_annotation_update(self, base_annotation: AnnotationV2) -> None:
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
        created_annotation = ANNOTATIONSAPI.create(base_annotation)
        try:
            annotation_update = AnnotationV2Update(id=created_annotation.id)
            for k, v in update.items():
                getattr(annotation_update, k).set(v)

            updated = ANNOTATIONSAPI.update([annotation_update])
            assert isinstance(updated, AnnotationV2List)
            updated = updated[0]
            for k, v in update.items():
                assert getattr(updated, k) == v
        finally:
            delete_with_check([created_annotation.id])

    def test_list(self, base_annotation: AnnotationV2, base_annotation2: AnnotationV2) -> None:
        cleanup()
        created_annotations = ANNOTATIONSAPI.create([base_annotation] * 30 + [base_annotation2] * 30)
        first_batch = created_annotations[:30]
        second_batch = created_annotations[30:]
        try:
            _test_list_on_created_annotations(first_batch, limit=-1)
            _test_list_on_created_annotations(second_batch, limit=-1)
        finally:
            delete_with_check([a.id for a in created_annotations])

    def test_list_limit(self, base_annotation: AnnotationV2) -> None:
        cleanup()
        created_annotations = ANNOTATIONSAPI.create([base_annotation] * 30)
        try:
            _test_list_on_created_annotations(created_annotations, limit=5)
            _test_list_on_created_annotations(created_annotations)
            _test_list_on_created_annotations(created_annotations, limit=30)
            _test_list_on_created_annotations(created_annotations, limit=-1)
        finally:
            delete_with_check([a.id for a in created_annotations])

    def test_retrieve(self, base_annotation: AnnotationV2) -> None:
        created_annotation = ANNOTATIONSAPI.create(base_annotation)
        try:
            retrieved_annotation = ANNOTATIONSAPI.retrieve(created_annotation.id)
            assert isinstance(retrieved_annotation, AnnotationV2)
            assert created_annotation.dump() == retrieved_annotation.dump()
        finally:
            delete_with_check([created_annotation.id])

    def test_retrieve_multiple(self, base_annotation: AnnotationV2List) -> None:
        created_annotations = ANNOTATIONSAPI.create([base_annotation] * 30)
        try:
            ids = [c.id for c in created_annotations]
            retrieved_annotations = ANNOTATIONSAPI.retrieve_multiple(ids)
            assert isinstance(retrieved_annotations, AnnotationV2List)

            # TODO assert the order and do without sorting
            # as soon as the API is fixed
            for ret, new in zip(
                sorted(retrieved_annotations, key=lambda a: a.id), sorted(created_annotations, key=lambda a: a.id)
            ):
                assert ret.dump() == new.dump()
        finally:
            delete_with_check([a.id for a in created_annotations])
