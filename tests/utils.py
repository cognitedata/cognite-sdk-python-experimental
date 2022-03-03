import gzip
import json
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Union

BASE_URL = "https://greenfield.cognitedata.com"


def jsgz_load(s):
    return json.loads(gzip.decompress(s).decode())


@contextmanager
def set_request_limit(client, limit):
    limits = [
        "_CREATE_LIMIT",
        "_LIST_LIMIT",
        "_RETRIEVE_LIMIT",
        "_UPDATE_LIMIT",
        "_DELETE_LIMIT",
        "_DPS_LIMIT",
        "_DPS_LIMIT_AGG",
        "_POST_DPS_OBJECTS_LIMIT",
        "_RETRIEVE_LATEST_LIMIT",
    ]

    tmp = {l: 0 for l in limits}
    for limit_name in limits:
        if hasattr(client, limit_name):
            tmp[limit_name] = getattr(client, limit_name)
            setattr(client, limit_name, limit)
    yield
    for limit_name, limit_val in tmp.items():
        if hasattr(client, limit_name):
            setattr(client, limit_name, limit_val)


@contextmanager
def unset_env_var(name: Union[str, List[str]]):
    if isinstance(name, str):
        name = [name]
    tmp = {}
    for n in name:
        tmp[n] = os.getenv(n)
        if tmp[n] is not None:
            del os.environ[n]
    yield
    for n in name:
        if tmp[n] is not None:
            os.environ[n] = tmp[n]


@contextmanager
def set_env_var(name: str, value: str):
    tmp = os.getenv(name)
    os.environ[name] = value
    yield
    if tmp is not None:
        os.environ[name] = tmp
    else:
        del os.environ[name]


def remove_None_from_nested_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    new_dict = {}
    for key, val in d.items():
        if isinstance(val, dict):
            val = remove_None_from_nested_dict(val)
        if val is not None:
            new_dict[key] = val
    return new_dict
