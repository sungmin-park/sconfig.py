import os
import re
import sys
from typing import Any, Dict, Type


def configure(module):
    if isinstance(module, str):
        module = sys.modules[module]

    for name, value in vars(module).items():
        if not re.match("^[A-Z_]+$", name):
            continue

        if name in os.environ:
            setattr(module, name, _convert(value, os.environ[name]))
        else:
            os.environ[name] = str(value)


# TODO add test case
def _convert(base, value):
    if base is True or base is False:
        if value:
            return value.lower() == 'true'
        return False

    if isinstance(base, str):
        return value

    if isinstance(base, int):
        return int(value)

    raise NotImplemented()


def sconfig(cls: Type[Any]) -> None:
    for name in _attrs(cls):
        if name in os.environ:
            setattr(cls, name, os.environ[name])


def _attrs(obj: Any) -> Dict[str, Any]:
    ret = {}
    for attr_name in dir(obj):
        if attr_name.startswith('_'):
            continue
        ret[attr_name] = getattr(obj, attr_name)
    return ret
