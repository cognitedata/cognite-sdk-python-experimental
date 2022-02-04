from functools import wraps

from cognite.client.utils._auxiliary import to_camel_case, to_snake_case


def use_v1_instead_of_playground(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        api_version = self._api_version
        self._api_version = "v1"
        result = f(self, *args, **kwargs)
        self._api_version = api_version
        return result

    return wrapper


def resource_to_camel_case(resource):
    if isinstance(resource, list):
        return [resource_to_camel_case(element) for element in resource]
    elif isinstance(resource, dict):
        return {to_camel_case(k): resource_to_camel_case(v) for k, v in resource.items() if v is not None}
    else:
        return resource


def resource_to_snake_case(resource):
    if isinstance(resource, list):
        return [resource_to_snake_case(element) for element in resource]
    elif isinstance(resource, dict):
        return {to_snake_case(k): resource_to_snake_case(v) for k, v in resource.items() if v is not None}
    else:
        return resource
