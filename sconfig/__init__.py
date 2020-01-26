import os
from typing import Any, Dict, Type, TypeVar, NewType, get_type_hints


def configure(cls: Type[Any]) -> str:
    hints = get_type_hints(cls)
    dumps = [f'* Simple Config - {cls.__name__}']

    for name in _attrs(cls):
        # looking for variables on env
        env_name = _to_env_name(cls.__name__, name)
        if env_name in os.environ:
            setattr(cls, name, os.environ[env_name])

        # check type hint. if type hint says it is secret, then do not dump the value
        hint = hints.get(name, None)
        if hint and getattr(hint, __SCONFIG_SECRET__, False):
            value = '[SECRET]'
        else:
            value = getattr(cls, name)

        dumps.append(f'    {name} = {value}')
    return '\n'.join(dumps)


T = TypeVar('T')

__SCONFIG_SECRET__ = '__sconfig_secret__'


def secret(type_: Type[T]) -> Type[T]:
    new_type = NewType(f'secret_{type_.__name__}', type_)
    setattr(new_type, __SCONFIG_SECRET__, True)
    return new_type


def _attrs(obj: Any) -> Dict[str, Any]:
    ret = {}
    for attr_name in dir(obj):
        if attr_name.startswith('_'):
            continue
        ret[attr_name] = getattr(obj, attr_name)
    return ret


def _to_env_name(config_name, property_name):
    return f'{config_name.upper()}_{property_name.upper()}'
