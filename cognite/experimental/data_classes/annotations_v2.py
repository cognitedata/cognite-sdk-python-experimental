import json
from typing import Any, Dict, List, Optional, Union

from cognite.client.data_classes._base import (
    CogniteFilter,
    CogniteObjectUpdate,
    CognitePrimitiveUpdate,
    CogniteResource,
    CogniteResourceList,
    CogniteUpdate,
)
from cognite.client.utils._auxiliary import to_snake_case


class AnnotationV2(CogniteResource):
    """Representation of an annotation in CDF.

    Args:
        annotation_type (str): Type name of the annotation type
        data (dict): The data payload containing the annotation information. Must match to the given annotation_type.
        status (str): The status of the annotation, e.g. "suggested", "approved", "rejected".
        
        annotated_resource_type (str): Type name of the CDF resource that is annotated, e.g. "file".
        annotated_resource_id (int, optional): The server-generated id of the CDF resource that is annotated. Defaults to None.
        annotated_resource_external_id (str, optional): The user-defined id of the CDF resource that is annotated. Defaults to None.

        creating_app (str): The name of the app from which this annotation was created.
        creating_app_version (str): The version of the app that created this annotation. Must be a valid semantic versioning (SemVer) string.
        creating_user: (str, optional): The user that created this annotation. Can be set to None, which means that the annotation was created by a service.[str] = None .

        linked_resource_type (str, optional): The CDF resource type of an optional linked CDF resource. Defaults to None.
        linked_resource_id (int, optional): The server-generated id of an optional linked CDF resource. Defaults to None.
        linked_resource_external_id (str, optional): The user-defined id of an optional linked CDF resource. Defaults to None.

        id (int, optional): A server-generated id for the object. Read only.
        created_time (int, optional): Time since this annotation was created in CDF. The time is measured in milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds. Read only.
        last_updated_time (int, optional): Time since this annotation was last updated in CDF. The time is measured in milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds. Read only.
        
        cognite_client (CogniteClient, optional): The client to associate with this object. Read only.
    """

    def __init__(
        self,
        annotation_type: str,
        data: dict,
        status: str,
        creating_app: str,
        creating_app_version: str,
        creating_user: Optional[str],
        annotated_resource_type: str,
        annotated_resource_id: Optional[int] = None,
        annotated_resource_external_id: Optional[str] = None,
        linked_resource_id: Optional[int] = None,
        linked_resource_external_id: Optional[str] = None,
        linked_resource_type: Optional[str] = None,
    ) -> None:
        self.annotation_type = annotation_type
        self.data = data
        self.status = status
        self.creating_app = creating_app
        self.creating_app_version = creating_app_version
        self.creating_user = creating_user
        self.annotated_resource_type = annotated_resource_type
        self.annotated_resource_id = annotated_resource_id
        self.annotated_resource_external_id = annotated_resource_external_id
        self.linked_resource_id = linked_resource_id
        self.linked_resource_external_id = linked_resource_external_id
        self.linked_resource_type = linked_resource_type
        self.id = None  # Read only
        self.created_time = None  # Read only
        self.last_updated_time = None  # Read only
        self._cognite_client = None  # Read only

    @classmethod
    def _load(cls, resource: Union[Dict[str, Any], str], cognite_client=None) -> "AnnotationV2":
        if isinstance(resource, str):
            return cls._load(json.loads(resource), cognite_client=cognite_client)
        elif isinstance(resource, dict):
            return cls.from_dict(resource, cognite_client=cognite_client)
        raise TypeError("Resource must be json str or Dict, not {}".format(type(resource)))

    @classmethod
    def from_dict(cls, resource: Dict[str, Any], cognite_client=None) -> "AnnotationV2":
        # Create base annotation
        data = {to_snake_case(key): val for key, val in resource.items()}
        annotation = AnnotationV2(
            annotation_type=data["annotation_type"],
            data=data["data"],
            status=data["status"],
            creating_app=data["creating_app"],
            creating_app_version=data["creating_app_version"],
            creating_user=data.get("creating_user"),
            annotated_resource_type=data["annotated_resource_type"],
            annotated_resource_id=data.get("annotated_resource_id"),
            annotated_resource_external_id=data.get("annotated_resource_external_id"),
            linked_resource_id=data.get("linked_resource_id"),
            linked_resource_external_id=data.get("linked_resource_external_id"),
            linked_resource_type=data.get("linked_resource_type"),
        )
        # Fill in read-only values, if available
        annotation.id = data.get("id")
        annotation.created_time = data.get("created_time")
        annotation.last_updated_time = data.get("last_updated_time")
        annotation._cognite_client = cognite_client
        return annotation

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        result = super().dump(camel_case=camel_case)
        # Special handling of created_user, which has a valid None value
        key = "creatingUser" if camel_case else "creating_user"
        result[key] = self.creating_user
        return result


class AnnotationV2Filter(CogniteFilter):
    """Filter on annotations with various criteria

    Args:
        annotated_resource_type (str): The type of the CDF resource that is annotated, e.g. "file".
        annotated_resource_ids (List[Dict[str, Any]]): List of ids and external ids of the annotated CDF resources to filter in. Example format: [{"id": 1234}, {"external_id": "ext_1234"}]. Must contain at least one item.
        status (str, optional): Status of annotations to filter for, e.g. "suggested", "approved", "rejected".
        creating_user (str, optional): Name of the user who created the annotations to filter for. Can be set explicitly to "None" to filter for annotations created by a service.
        creating_app (str, optional): Name of the app from which the annotations to filter for where created. 
        creating_app_version (str, optional): Version of the app from which the annotations to filter for were created.
        linked_resource_type(str, optional): Type of the CDF resource the annotations to filter for are linked to, if any.
        linked_resource_ids(List[Dict[str, Any]], optional): List of ids or external ids the annotations are linked to. Example format: [{"id": 1234}, {"external_id": "ext_1234"}] .
        annotation_type(str, optional): Type name of the annotations.
    """

    def __init__(
        self,
        annotated_resource_type: str,
        annotated_resource_ids: List[Dict[str, Any]],
        status: Optional[str] = None,
        creating_user: Optional[str] = "",  # None means filtering for a service
        creating_app: Optional[str] = None,
        creating_app_version: Optional[str] = None,
        linked_resource_type: Optional[str] = None,
        linked_resource_ids: Optional[List[Dict[str, Any]]] = None,
        annotation_type: Optional[str] = None,
    ) -> None:
        self.annotated_resource_type = annotated_resource_type
        self.annotated_resource_ids = annotated_resource_ids
        self.status = status
        self.creating_user = creating_user
        self.creating_app = creating_app
        self.creating_app_version = creating_app_version
        self.linked_resource_type = linked_resource_type
        self.linked_resource_ids = linked_resource_ids
        self.annotation_type = annotation_type
        self._cognite_client = (
            None  # Read only. Will be filled by superclass load. # TODO is this true? Will this ever be used?
        )

    def dump(self, camel_case: bool = False):
        result = super(AnnotationV2Filter, self).dump(camel_case=camel_case)
        # Special handling for creating_user, which hasa valid None value
        key = "creatingUser" if camel_case else "creating_user"
        # Remove creating_user if it is an empty string
        if self.creating_user == "":
            del result[key]
        # dump creating_user if it is None
        elif self.creating_user is None:
            result[key] = None
        return result


class AnnotationV2Update(CogniteUpdate):
    """Changes applied to annotation

    Args:
        id (int): A server-generated ID for the object.
    """

    def __init__(self, id: int):
        super().__init__(id=id)

    class _StrUpdate(CognitePrimitiveUpdate):
        """ Only set, no set_null """

        def set(self, value: str) -> "AnnotationV2Update":
            return self._set(value)

    class _OptionalStrUpdate(CognitePrimitiveUpdate):
        """ Set and set_null """

        def set(self, value: Optional[str]) -> "AnnotationV2Update":
            return self._set(value)

    class _DictUpdate(CogniteObjectUpdate):
        """ Only set, no set_null """

        def set(self, value: Dict[str, Any]) -> "AnnotationV2Update":
            return self._set(value)

    class _OptionalIntUpdate(CognitePrimitiveUpdate):
        """ Set and set_null """

        def set(self, value: Optional[int]) -> "AnnotationV2Update":
            return self._set(value)

    @property
    def data(self) -> "AnnotationV2Update._DictUpdate":
        return AnnotationV2Update._DictUpdate(self, "data")

    @property
    def status(self) -> "AnnotationV2Update._StrUpdate":
        return AnnotationV2Update._StrUpdate(self, "status")

    @property
    def annotation_type(self) -> "AnnotationV2Update._StrUpdate":
        return AnnotationV2Update._StrUpdate(self, "annotationType")

    @property
    def linked_resource_type(self) -> "AnnotationV2Update._OptionalStrUpdate":
        return AnnotationV2Update._OptionalStrUpdate(self, "linkedResourceType")

    @property
    def linked_resource_id(self) -> "AnnotationV2Update._OptionalIntUpdate":
        return AnnotationV2Update._OptionalIntUpdate(self, "linkedResourceId")

    @property
    def linked_resource_external_id(self) -> "AnnotationV2Update._OptionalStrUpdate":
        return AnnotationV2Update._OptionalStrUpdate(self, "linkedResourceExternalId")


class AnnotationV2List(CogniteResourceList):
    _RESOURCE = AnnotationV2
    _UPDATE = AnnotationV2Update