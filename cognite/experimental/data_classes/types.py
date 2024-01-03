from __future__ import annotations

from typing import Any, Dict

from cognite.client.data_classes._base import (
    CogniteFilter,
    CognitePropertyClassUtil,
    CogniteResource,
    CogniteResourceList,
)


class TypeDefinitionReference(dict):
    pass


# GenPropertyClass: ParentTypeDefinitionFilter
class ParentTypeDefinitionFilter(dict):
    """filter for type definitions that belong to the subtree defined by the root parent type specified

    Args:
        id (int): A server-generated ID for the object.
        version (int): A server-generated ID for the object.
        external_id (str): External Id provided by client. Should be unique within the project.
    """

    def __init__(self, id: int | None = None, version: int | None = None, external_id: str | None = None, **kwargs):
        self.id = id
        self.version = version
        self.external_id = external_id
        self.update(kwargs)

    id = CognitePropertyClassUtil.declare_property("id")
    version = CognitePropertyClassUtil.declare_property("version")
    external_id = CognitePropertyClassUtil.declare_property("externalId")

    # GenStop


# GenClass: TypeDefinitionSpec, TypeDefinition
class Type(CogniteResource):
    """No description.

    Args:
        external_id (str): External Id provided by client. Should be unique within the project.
        name (str): No description.
        description (str): No description.
        properties (List[Dict[str, Any]]): No description.
        parent_type (Union[Dict[str, Any], TypeDefinitionReference]): No description.
        id (int): A server-generated ID for the object.
        version (int): A server-generated ID for the object.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        external_id: str | None = None,
        name: str | None = None,
        description: str | None = None,
        properties: list[dict[str, Any]] | None = None,
        parent_type: dict[str, Any] | TypeDefinitionReference | None = None,
        id: int | None = None,
        version: int | None = None,
        created_time: int | None = None,
        last_updated_time: int | None = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.name = name
        self.description = description
        self.properties = properties
        self.parent_type = parent_type
        self.id = id
        self.version = version
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: dict | str, cognite_client=None):
        instance = super()._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.parent_type is not None:
                instance.parent_type = TypeDefinitionReference(**instance.parent_type)
        return instance

    # GenStop


# GenClass: TypeDefinitionFilter.filter
class TypeFilter(CogniteFilter):
    """Filter on types with strict matching.

    Args:
        name (str): Returns the type definitions matching that name.
        external_id_prefix (str): filter external ids starting with the prefix specified
        type_subtree (Union[Dict[str, Any], ParentTypeDefinitionFilter]): filter for type definitions that belong to the subtree defined by the root parent type specified
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        name: str | None = None,
        external_id_prefix: str | None = None,
        type_subtree: dict[str, Any] | ParentTypeDefinitionFilter | None = None,
        cognite_client=None,
    ):
        self.name = name
        self.external_id_prefix = external_id_prefix
        self.type_subtree = type_subtree
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: dict | str, cognite_client=None):
        instance = super()._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.type_subtree is not None:
                instance.type_subtree = ParentTypeDefinitionFilter(**instance.type_subtree)
        return instance

    # GenStop


class TypeList(CogniteResourceList):
    _RESOURCE = Type
    _UPDATE = None
    _ASSERT_CLASSES = False  # because no Update
