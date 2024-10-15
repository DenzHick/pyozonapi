from typing import (
    Union,
    Any,
    Dict,
    List
)
from math import ceil

def list_division(_list: Union[list, str], divider: int) -> list:
    result = []

    if len(_list) == 0:
        return result

    for i in range(ceil(len(_list) / divider)):
        if (i + 1) * divider > len(_list):
            result.append(_list[i * divider:len(_list)])
        else:
            result.append(_list[i * divider:(i + 1) * divider])
    return result

def add_values(model: object, data: Dict[str, Any], exc: List[str] = []):
    for key, value in data.items():
        if (not hasattr(model, key)) and (key not in exc):
            setattr(model, key, value)
