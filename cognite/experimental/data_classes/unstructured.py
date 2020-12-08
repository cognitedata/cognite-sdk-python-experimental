import json
from typing import Any, Dict, List

from cognite.client.data_classes import TimestampRange
from cognite.client.data_classes._base import *

from cognite.experimental.data_classes.shared import AssetIdsFilter, GeoShape


# GenClass: SearchHighlight
class UnstructuredSearchHighlight(CogniteResource):
    """No description.

    Args:
        external_id (List[str]): Matches in externalId.
        name (List[str]): Matches in name.
        content (List[str]): Matches in content.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self, external_id: List[str] = None, name: List[str] = None, content: List[str] = None, cognite_client=None
    ):
        self.external_id = external_id
        self.name = name
        self.content = content
        self._cognite_client = cognite_client

    # GenStop


# GenClass: FilesMetadata
class UnstructuredFileMetadata(CogniteResource):
    """No description.

    Args:
        external_id (str): External Id provided by client. Should be unique within the project.
        name (str): Name of the file.
        source (str): The source of the file
        mime_type (str): File type. E.g. 'text/plain', 'application/pdf'.
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Maximum length of key is 32 bytes, value 512 bytes, up to 16 key-value pairs.
        asset_ids (List[int]): No description.
        source_created_time (int): The timestamp for when the file was originally created in the source system.
        source_modified_time (int): The timestamp for when the file was last modified in the source system.
        id (int): A server-generated ID for the object.
        uploaded_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        created_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        last_updated_time (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
        indices (List[str]): All indices this document belongs to
        document_types (List[str]): All document types this document has been classified as
        language (str): Detected language from file content.
        geolocation (Union[Dict[str, Any], GeoShape]): GeoJson representation of a geometry.
        data_set_id (int): A server-generated ID for the object.
        security_categories (List[int]): The security category IDs required to access this file.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        external_id: str = None,
        name: str = None,
        source: str = None,
        mime_type: str = None,
        metadata: Dict[str, str] = None,
        asset_ids: List[int] = None,
        source_created_time: int = None,
        source_modified_time: int = None,
        id: int = None,
        uploaded_time: int = None,
        created_time: int = None,
        last_updated_time: int = None,
        indices: List[str] = None,
        document_types: List[str] = None,
        language: str = None,
        geolocation: Union[Dict[str, Any], GeoShape] = None,
        data_set_id: int = None,
        security_categories: List[int] = None,
        cognite_client=None,
    ):
        self.external_id = external_id
        self.name = name
        self.source = source
        self.mime_type = mime_type
        self.metadata = metadata
        self.asset_ids = asset_ids
        self.source_created_time = source_created_time
        self.source_modified_time = source_modified_time
        self.id = id
        self.uploaded_time = uploaded_time
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.indices = indices
        self.document_types = document_types
        self.language = language
        self.geolocation = geolocation
        self.data_set_id = data_set_id
        self.security_categories = security_categories
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(UnstructuredFileMetadata, cls)._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.geolocation is not None:
                instance.geolocation = GeoShape(**instance.geolocation)
        return instance

    # GenStop


class UnstructuredSearchResult(CogniteResource):
    def __init__(self, highlight: Dict[str, Any] = None, item: Dict[str, str] = None, cognite_client=None):
        """Unstructured Search Result

        Args:
            item (Dict[str, str]): The search result. Will be converted to a UnstructuredFileMetadata.
            highlight (Dict[str, Any]): Highlighted snippets from content, name and externalId fields which show where the query matches are. Converted to UnstructuredSearchHighlight.
            cognite_client (CogniteClient): The client to associate with this object.
        """
        self.highlight = None
        if highlight:
            self.highlight = UnstructuredSearchHighlight._load(highlight, cognite_client=self._cognite_client)
        self.item = UnstructuredFileMetadata._load(item, cognite_client=self._cognite_client)
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        if isinstance(resource, str):
            resource = json.loads(resource)
        return cls(item=resource["item"], highlight=resource.get("highlight"), cognite_client=cognite_client)

    def dump(self, camel_case: bool = False) -> Dict[str, Any]:
        itemdump = self.item.dump(camel_case=camel_case)
        if self.highlight:
            itemdump["highlight"] = self.highlight.dump(camel_case=camel_case)
        return itemdump


# GenClass: UnstructuredAggregateResult
class UnstructuredAggregate(CogniteResource):
    """No description.

    Args:
        name (str): User defined name for this aggregate
        groups (List[Dict[str, Any]]): No description.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(self, name: str = None, groups: List[Dict[str, Any]] = None, cognite_client=None):
        self.name = name
        self.groups = groups
        self._cognite_client = cognite_client

    # GenStop


class UnstructuredSearchHighlightList(CogniteResourceList):
    _RESOURCE = UnstructuredSearchHighlight
    _UPDATE = None
    _ASSERT_CLASSES = False


class UnstructuredFileMetadataList(CogniteResourceList):
    _RESOURCE = UnstructuredFileMetadata
    _UPDATE = None
    _ASSERT_CLASSES = False


class UnstructuredAggregateList(CogniteResourceList):
    _RESOURCE = UnstructuredAggregate
    _UPDATE = None
    _ASSERT_CLASSES = False


class UnstructuredSearchResultList(CogniteResourceList):
    _RESOURCE = UnstructuredSearchResult
    _UPDATE = None
    _ASSERT_CLASSES = False

    def __init__(
        self,
        resources: List[UnstructuredSearchResult],
        cognite_client=None,
        aggregates: UnstructuredAggregateList = None,
    ):
        super().__init__(resources, cognite_client)
        self.aggregates = aggregates

    @property
    def files(self):
        return UnstructuredFileMetadataList([res.item for res in self], cognite_client=self._cognite_client)

    @property
    def highlights(self):
        if not any(res.highlight for res in self):
            raise ValueError("No highlights are available in this search result.")
        return UnstructuredSearchHighlightList([res.highlight for res in self], cognite_client=self._cognite_client)


# GenClass: FileFilter.filter
class UnstructuredSearchFileFilter(CogniteFilter):
    """No description.

    Args:
        name (Dict[str, str]): Name of the file.
        mime_type (Dict[str, str]): File type. E.g. 'text/plain', 'application/pdf'.
        metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value. Limits: Maximum length of key is 32 bytes, value 512 bytes, up to 16 key-value pairs.
        asset_ids (Union[Dict[str, Any], AssetIdsFilter]): Only include files that reference these specific asset IDs.
        source (Dict[str, str]): The source of the file.
        created_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        last_updated_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        uploaded_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        source_created_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        source_modified_time (Union[Dict[str, Any], TimestampRange]): Range between two timestamps.
        geolocation (Dict[str, Any]): Filter for files where
        indices (Dict[str, Any]): Filter for indices
        document_types (Dict[str, Any]): Filter for document types
        data_set_id (Dict[str, str]): No description.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        name: Dict[str, str] = None,
        mime_type: Dict[str, str] = None,
        metadata: Dict[str, str] = None,
        asset_ids: Union[Dict[str, Any], AssetIdsFilter] = None,
        source: Dict[str, str] = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        last_updated_time: Union[Dict[str, Any], TimestampRange] = None,
        uploaded_time: Union[Dict[str, Any], TimestampRange] = None,
        source_created_time: Union[Dict[str, Any], TimestampRange] = None,
        source_modified_time: Union[Dict[str, Any], TimestampRange] = None,
        geolocation: Dict[str, Any] = None,
        indices: Dict[str, Any] = None,
        document_types: Dict[str, Any] = None,
        data_set_id: Dict[str, str] = None,
        cognite_client=None,
    ):
        self.name = name
        self.mime_type = mime_type
        self.metadata = metadata
        self.asset_ids = asset_ids
        self.source = source
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.uploaded_time = uploaded_time
        self.source_created_time = source_created_time
        self.source_modified_time = source_modified_time
        self.geolocation = geolocation
        self.indices = indices
        self.document_types = document_types
        self.data_set_id = data_set_id
        self._cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(UnstructuredSearchFileFilter, cls)._load(resource, cognite_client)
        if isinstance(resource, Dict):
            if instance.asset_ids is not None:
                instance.asset_ids = AssetIdsFilter(**instance.asset_ids)
            if instance.created_time is not None:
                instance.created_time = TimestampRange(**instance.created_time)
            if instance.last_updated_time is not None:
                instance.last_updated_time = TimestampRange(**instance.last_updated_time)
            if instance.uploaded_time is not None:
                instance.uploaded_time = TimestampRange(**instance.uploaded_time)
            if instance.source_created_time is not None:
                instance.source_created_time = TimestampRange(**instance.source_created_time)
            if instance.source_modified_time is not None:
                instance.source_modified_time = TimestampRange(**instance.source_modified_time)
        return instance

    # GenStop
