from typing import List, Optional

import pytest
from cognite.client.data_classes import FileMetadata
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import AnnotationV2, AnnotationV2Filter, AnnotationV2List, AnnotationV2Update
from tests.utils import remove_None_from_nested_dict


def delete_with_check(
    cognite_client: CogniteClient, delete_ids: List[int], check_ids: Optional[List[int]] = None
) -> None:
    if check_ids is None:
        check_ids = delete_ids
    cognite_client.annotations_v2.delete(id=delete_ids)
    try:
        cognite_client.annotations_v2.retrieve_multiple(check_ids)
        raise ValueError(f"retrieve_multiple after delete successful for ids {check_ids}")
    except CogniteAPIError as e:
        assert e.code == 404
        missing = [i["id"] for i in e.missing]
        assert sorted(check_ids) == sorted(missing)


@pytest.fixture(scope="class")
def cognite_client() -> CogniteClient:
    return CogniteClient()


@pytest.fixture
def file_id(cognite_client: CogniteClient) -> int:
    # Create a test file
    name = "annotation_v2_unit_test_file"
    file = cognite_client.files.create(FileMetadata(external_id=name, name=name), overwrite=True)[0]
    yield file.id
    # Teardown all annotations to the file
    filter = AnnotationV2Filter(
        annotated_resource_type="file",
        annotated_resource_ids=[{"id": file.id}],
        creating_app="UnitTest",
    )
    annotation_ids = [a.id for a in cognite_client.annotations_v2.list(filter=filter)]
    if annotation_ids:
        delete_with_check(cognite_client, annotation_ids)
    # Teardown the file itself
    cognite_client.files.delete(id=file.id)


@pytest.fixture
def base_annotation(annotation: AnnotationV2, file_id: int):
    annotation.annotated_resource_id = file_id
    return annotation


def check_created_vs_base(base_annotation: AnnotationV2, created_annotation: AnnotationV2) -> None:
    base_dump = base_annotation.dump()
    created_dump = created_annotation.dump()
    special_keys = ["id", "created_time", "last_updated_time", "data"]
    found_special_keys = 0
    for k, v in created_dump.items():
        if k in special_keys:
            found_special_keys += 1
            assert v is not None
        else:
            assert v == base_dump[k]
    assert found_special_keys == len(special_keys)
    # assert data is equal, except None fields
    created_dump_data = remove_None_from_nested_dict(created_dump["data"])
    base_dump_data = remove_None_from_nested_dict(base_dump["data"])
    assert created_dump_data == base_dump_data


def _test_list_on_created_annotations(cognite_client: CogniteClient, annotations: AnnotationV2List, limit: int = 25):
    annotation = annotations[0]
    filter = AnnotationV2Filter(
        annotated_resource_type=annotation.annotated_resource_type,
        annotated_resource_ids=[{"id": annotation.annotated_resource_id}],
        status=annotation.status,
        creating_app=annotation.creating_app,
        creating_app_version=annotation.creating_app_version,
        creating_user=annotation.creating_user,
    )
    annotations_list = cognite_client.annotations_v2.list(filter=filter, limit=limit)
    assert isinstance(annotations_list, AnnotationV2List)
    if limit == -1 or limit > len(annotations):
        assert len(annotations_list) == len(annotations)
    else:
        assert len(annotations_list) == limit

    for a in annotations_list:
        check_created_vs_base(annotation, a)


class TestAnnotationsV2Integration:
    def test_create_single_annotation(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotation = cognite_client.annotations_v2.create(base_annotation)
        assert isinstance(created_annotation, AnnotationV2)
        check_created_vs_base(base_annotation, created_annotation)
        assert created_annotation.creating_user == None

    def test_create_single_annotation2(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        base_annotation.status = "rejected"
        base_annotation.creating_user = "unit.test@cognite.com"
        created_annotation = cognite_client.annotations_v2.create(base_annotation)
        assert isinstance(created_annotation, AnnotationV2)
        check_created_vs_base(base_annotation, created_annotation)
        assert created_annotation.creating_user == "unit.test@cognite.com"

    def test_create_annotations(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotations = cognite_client.annotations_v2.create([base_annotation] * 30)
        assert isinstance(created_annotations, AnnotationV2List)
        for a in created_annotations:
            check_created_vs_base(base_annotation, a)

    def test_delete_annotations(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotations = cognite_client.annotations_v2.create([base_annotation] * 30)
        delete_with_check(cognite_client, [a.id for a in created_annotations])

    def test_update_annotation_by_annotation(
        self, cognite_client: CogniteClient, base_annotation: AnnotationV2
    ) -> None:
        # Create annotation, make some local changes and cache a dump
        annotation = cognite_client.annotations_v2.create(base_annotation)
        annotation.linked_resource_type = "asset"
        annotation.linked_resource_id = 1
        local_dump = annotation.dump()
        # Update the annotation on remote and make a dump
        annotation = cognite_client.annotations_v2.update(annotation)
        assert isinstance(annotation, AnnotationV2)
        # Check that the local dump matches the remove dump
        remote_dump = annotation.dump()
        for k, v in remote_dump.items():
            if k == "last_updated_time":
                assert v > local_dump[k]
            else:
                assert v == local_dump[k]

    def test_update_annotation_by_annotation_update(
        self, cognite_client: CogniteClient, base_annotation: AnnotationV2
    ) -> None:
        update = {
            "data": {
                "pageNumber": 1,
                "assetRef": {"id": 1, "externalId": None},
                "textRegion": {"xMin": 0.5, "xMax": 1.0, "yMin": 0.5, "yMax": 1.0, "confidence": None},
                "text": "AB-CX-DE",
                "symbolRegion": {"xMin": 0.0, "xMax": 0.5, "yMin": 0.5, "yMax": 1.0, "confidence": None},
                "symbol": "pump",
            },
            "status": "rejected",
            "annotation_type": "diagrams.AssetLink",
            "linked_resource_type": "asset",
            "linked_resource_id": 1,
            "linked_resource_external_id": None,
        }
        created_annotation = cognite_client.annotations_v2.create(base_annotation)

        annotation_update = AnnotationV2Update(id=created_annotation.id)
        for k, v in update.items():
            getattr(annotation_update, k).set(v)

        updated = cognite_client.annotations_v2.update([annotation_update])
        assert isinstance(updated, AnnotationV2List)
        updated = updated[0]
        for k, v in update.items():
            assert getattr(updated, k) == v

    def test_list(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotations_1 = cognite_client.annotations_v2.create([base_annotation] * 30)
        base_annotation.status = "rejected"
        created_annotations_2 = cognite_client.annotations_v2.create([base_annotation] * 30)
        _test_list_on_created_annotations(cognite_client, created_annotations_1, limit=-1)
        _test_list_on_created_annotations(cognite_client, created_annotations_2, limit=-1)

    def test_list_limit(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotations = cognite_client.annotations_v2.create([base_annotation] * 30)
        _test_list_on_created_annotations(cognite_client, created_annotations, limit=5)
        _test_list_on_created_annotations(cognite_client, created_annotations)
        _test_list_on_created_annotations(cognite_client, created_annotations, limit=30)
        _test_list_on_created_annotations(cognite_client, created_annotations, limit=-1)

    def test_retrieve(self, cognite_client: CogniteClient, base_annotation: AnnotationV2) -> None:
        created_annotation = cognite_client.annotations_v2.create(base_annotation)
        retrieved_annotation = cognite_client.annotations_v2.retrieve(created_annotation.id)
        assert isinstance(retrieved_annotation, AnnotationV2)
        assert created_annotation.dump() == retrieved_annotation.dump()

    def test_retrieve_multiple(self, cognite_client: CogniteClient, base_annotation: AnnotationV2List) -> None:
        created_annotations = cognite_client.annotations_v2.create([base_annotation] * 30)
        ids = [c.id for c in created_annotations]
        retrieved_annotations = cognite_client.annotations_v2.retrieve_multiple(ids)
        assert isinstance(retrieved_annotations, AnnotationV2List)

        # TODO assert the order and do without sorting
        # as soon as the API is fixed
        for ret, new in zip(
            sorted(retrieved_annotations, key=lambda a: a.id), sorted(created_annotations, key=lambda a: a.id)
        ):
            assert ret.dump() == new.dump()
