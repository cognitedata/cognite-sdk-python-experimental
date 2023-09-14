import gzip
import json
from typing import Any, Dict

BASE_URL = "https://greenfield.cognitedata.com"


def jsgz_load(s):
    return json.loads(gzip.decompress(s).decode())


def remove_None_from_nested_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    new_dict = {}
    for key, val in d.items():
        if isinstance(val, dict):
            val = remove_None_from_nested_dict(val)
        if val is not None:
            new_dict[key] = val
    return new_dict
