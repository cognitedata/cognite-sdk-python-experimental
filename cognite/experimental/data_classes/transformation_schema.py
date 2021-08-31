from cognite.client.data_classes._base import *


class TransformationSchemaType:
    def __init__(self, type: str = None):
        self.type = type


class TransformationSchemaArrayType(TransformationSchemaType):
    def __init__(self, type: str = None, element_type: str = None, contains_null: bool = False):
        super().__init__(type=type)
        self.element_type = element_type
        self.contains_null = contains_null


class TransformationSchemaMapType(TransformationSchemaType):
    def __init__(self, type: str, key_type: str = None, value_type: str = None, value_contains_null: bool = False):
        super().__init__(type=type)
        self.key_type = key_type
        self.value_type = value_type
        self.value_contains_null = value_contains_null


class TransformationSchemaColumn(CogniteResource):
    """Transformation schema column represents a column of the expected sql structure for a destination type.

    Args:
        request_scheduler_id: Id of the schedule in request scheduler service.
        id (int): Transformation id.
        external_id (str): Transformation externalId.
        created_time (int): Time when the schedule was created.
        last_updated_time (int): Time when the schedule was last updated.
        interval (str): Cron expression describes when the function should be called. Use http://www.cronmaker.com to create a cron expression.
        is_paused (bool): If true, the transformation is not scheduled.
        cognite_client (CogniteClient): The client to associate with this object.
    """

    def __init__(
        self,
        name: str = None,
        sql_type: str = None,
        type: TransformationSchemaType = None,
        nullable: bool = False,
        cognite_client=None,
    ):
        self.name = name
        self.sql_type = sql_type
        self.type = type
        self.nullable = nullable
        self.cognite_client = cognite_client

    @classmethod
    def _load(cls, resource: Union[Dict, str], cognite_client=None):
        instance = super(TransformationSchemaColumn, cls)._load(resource, cognite_client)
        if isinstance(instance.type, Dict):
            snake_dict = {utils._auxiliary.to_snake_case(key): value for (key, value) in instance.type.items()}
            instance_type = instance.type.get("type")
            if instance_type == "array":
                instance.type = TransformationSchemaArrayType(**snake_dict)
            elif instance_type == "map":
                instance.type = TransformationSchemaMapType(**snake_dict)
        elif isinstance(instance.type, str):
            instance.type = TransformationSchemaType(type=instance.type)
        return instance

    def __hash__(self):
        return hash(self.request_scheduler_id)


class TransformationSchemaColumnList(CogniteResourceList):
    _RESOURCE = TransformationSchemaColumn
    _ASSERT_CLASSES = False
