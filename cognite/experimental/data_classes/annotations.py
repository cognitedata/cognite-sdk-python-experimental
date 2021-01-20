from cognite.client.data_classes._base import CogniteFilter, CogniteResource, CogniteResourceList, CogniteUpdate


class Annotation(CogniteResource):
    """Representation of an annotation in CDF.

    Args:
        id (int, optional): [description]. Defaults to None.
        annotated_resource_id (int, optional): [description]. Defaults to None.
        text (str, optional): [description]. Defaults to None.
        annotated_resource_external_id (str, optional): [description]. Defaults to None.
        annotated_resource_type (str, optional): [description]. Defaults to None.
        linked_resource_id (int, optional): [description]. Defaults to None.
        linked_resource_external_id (str, optional): [description]. Defaults to None.
        linked_resource_type (str, optional): [description]. Defaults to None.
        annotation_type (str, optional): [description]. Defaults to None.
        status (str, optional): [description]. Defaults to None.
        source (str, optional): [description]. Defaults to None.
        region ([type], optional): [description]. Defaults to None.
        data ([type], optional): [description]. Defaults to None.
        created_time (int, optional): Time, in milliseconds since Jan. 1, 1970, when this annotation was created in CDF
        last_updated_time (int, optional): Time, in milliseconds since Jan. 1, 1970, when this annotation was last updated in CDF.
        cognite_client ([type], optional): The client to associate with this object.
    """

    def __init__(
        self,
        id: int = None,
        annotated_resource_id: int = None,
        text: str = None,
        annotated_resource_external_id: str = None,
        annotated_resource_type: str = None,
        linked_resource_id: int = None,
        linked_resource_external_id: str = None,
        linked_resource_type: str = None,
        annotation_type: str = None,
        status: str = None,
        source: str = None,
        region=None,
        data=None,
        created_time: int = None,
        last_updated_time: int = None,
        cognite_client=None,
    ):
        self.id = id
        self.annotated_resource_id = annotated_resource_id
        self.text = text
        self.annotated_resource_external_id = annotated_resource_external_id
        self.annotated_resource_type = annotated_resource_type
        self.linked_resource_id = linked_resource_id
        self.linked_resource_external_id = linked_resource_external_id
        self.linked_resource_type = linked_resource_type
        self.annotation_type = annotation_type
        self.status = status
        self.source = source
        self.region = region
        self.data = data
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self._cognite_client = cognite_client


class AnnotationFilter(CogniteFilter):
    def __init__(self, annotation_type: str = None, annotated_resource_ids: list = None):
        self.annotation_type = annotation_type
        self.annotated_resource_ids = annotated_resource_ids


class AnnotationUpdate(CogniteUpdate):
    pass


class AnnotationList(CogniteResourceList):
    _RESOURCE = Annotation
    _UPDATE = AnnotationUpdate
