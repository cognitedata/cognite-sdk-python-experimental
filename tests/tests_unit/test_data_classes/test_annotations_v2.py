import json
from copy import deepcopy
from typing import Optional

import pytest
from cognite.client.utils._auxiliary import to_snake_case

from cognite.experimental.data_classes import AnnotationV2, AnnotationV2Filter, AnnotationV2Update, annotations_v2


class TestAnnotationV2:
    @pytest.mark.parametrize(
        "creating_user, camel_case",
        [("john.doe@cognite.com", False), ("john.doe@cognite.com", True), (None, False), (None, True),],
        ids=["snake_case", "camel_case", "snake_case_None", "camel_case_None"],
    )
    def test_dump(self, annotation: AnnotationV2, creating_user: Optional[str], camel_case: bool) -> None:
        annotation = deepcopy(annotation)
        annotation.creating_user = creating_user
        super_dump = super(AnnotationV2, annotation).dump(camel_case=camel_case)
        dump = annotation.dump(camel_case=camel_case)
        key = "creatingUser" if camel_case else "creating_user"
        for k, v in dump.items():
            if k == key:
                assert v == creating_user
            else:
                # No key except creating_user can be None
                assert v is not None
                # Must match the super_dump for all other fields
                assert v == super_dump[k]

    def test_load(self, annotation: AnnotationV2) -> None:
        resource = json.dumps(annotation.dump(camel_case=True))
        loaded_annotation = AnnotationV2._load(resource, cognite_client=None)
        assert annotation == loaded_annotation


class TestAnnotationV2Filter:
    @pytest.mark.parametrize(
        "creating_user, camel_case",
        [
            ("john.doe@cognite.com", False),
            ("john.doe@cognite.com", True),
            (None, False),
            (None, True),
            ("", False),
            ("", True),
        ],
        ids=["snake_case", "camel_case", "snake_case_None", "camel_case_None", "snake_case_empty", "camel_case_empty"],
    )
    def test_dump(self, annotation_filter: AnnotationV2Filter, creating_user: Optional[str], camel_case: bool) -> None:
        annotation_filter = deepcopy(annotation_filter)
        annotation_filter.creating_user = creating_user
        super_dump = super(AnnotationV2Filter, annotation_filter).dump(camel_case=camel_case)
        dump = annotation_filter.dump(camel_case=camel_case)
        key = "creatingUser" if camel_case else "creating_user"
        for k, v in dump.items():
            if k == key:
                assert v == creating_user
            else:
                # No key except creating_user can be None
                assert v is not None
                # Must match the super_dump for all other fields
                assert v == super_dump[k]


class TestAnnotationV2Update:
    def test_set_chain(self):
        update = {
            "data": {"assetRef": {"id": 1}, "textRegion": {"xMin": 0.0, "xMax": 0.5, "yMin": 0.5, "yMax": 1.0,}},
            "status": "rejected",
            "annotationType": "diagrams.AssetLink",
            "linkedResourceType": "asset",
            "linkedResourceId": 1,
            "linkedResourceExternalId": None,
        }
        annotation_update = AnnotationV2Update(id=1)
        for k, v in update.items():
            snake_case_key = to_snake_case(k)
            getattr(annotation_update, snake_case_key).set(v)
            if v is None:
                update[k] = {"setNull": True}
            else:
                update[k] = {"set": v}

        annotation_update_dump = annotation_update.dump()
        assert annotation_update_dump["id"] == 1
        assert annotation_update_dump["update"] == update