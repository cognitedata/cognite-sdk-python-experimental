from functools import wraps


def use_v1_instead_of_playground(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        api_version = self._api_version
        self._api_version = "v1"
        result = f(self, *args, **kwargs)
        self._api_version = api_version
        return result

    return wrapper
