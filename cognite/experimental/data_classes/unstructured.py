from typing import Any, Dict, List

from cognite.client.data_classes import TimestampRange
from cognite.client.data_classes._base import *
from cognite.experimental.data_classes.shared import AssetIdsFilter


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


class UnstructuredSearchHighlightList(CogniteResourceList):
    _RESOURCE = UnstructuredSearchHighlight
    _UPDATE = None
    _ASSERT_CLASSES = False


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
        uploaded (bool): Whether or not the actual file is uploaded. This field is returned only by the API, it has no effect in a post body.
        geolocation (Dict[str, Any]): Filter for files where
        indices (Dict[str, Any]): Filter for indices
        document_types (Dict[str, Any]): Filter for document types
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
        uploaded: bool = None,
        geolocation: Dict[str, Any] = None,
        indices: Dict[str, Any] = None,
        document_types: Dict[str, Any] = None,
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
        self.uploaded = uploaded
        self.geolocation = geolocation
        self.indices = indices
        self.document_types = document_types
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
