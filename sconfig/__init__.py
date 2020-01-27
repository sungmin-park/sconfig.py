import os
from pathlib import Path
from typing import Any, Dict, Type, TypeVar, NewType, get_type_hints

import toml
from stringcase import snakecase, uppercase


def configure(cls: Type[Any]) -> str:
    hints = get_type_hints(cls)
    config_name = cls.__name__
    env_config_name = _to_env_config_name(config_name)

    toml_config = {}
    config_file_name = os.environ.get(
        f'SCONFIG_{env_config_name}', 'sconfig.toml'
    )
    if Path(config_file_name).is_file():
        with open(config_file_name, 'r') as f:
            whole_toml = toml.loads(f.read())
            toml_config = whole_toml.get(config_name, {})

    ret_toml_config = {}
    ret_env_config = {}
    for name in _attrs(cls):
        hint = hints.get(name, None)

        # looking for variables on toml file
        if name in toml_config:
            setattr(cls, name, toml_config[name])

        # looking for variables on env
        env_name = _to_env_name(config_name, name)
        if env_name in os.environ:
            setattr(cls, name, os.environ[env_name])
        if hint and _hasattr_r(hint, __SCONFIG_ENV_OVERRIDE_NAME__):
            override_env_name = _getattr_r(hint, __SCONFIG_ENV_OVERRIDE_NAME__, None)
            if override_env_name and override_env_name in os.environ:
                setattr(cls, name, os.environ[override_env_name])
                env_name = override_env_name

        # check type hint. if type hint says it is secret, then do not dump the value
        if hint and _getattr_r(hint, __SCONFIG_SECRET__, False):
            value = '[SECRET]'
        else:
            value = getattr(cls, name)

        ret_toml_config[name] = value
        ret_env_config[env_name] = value

    return toml.dumps({config_name: ret_toml_config, env_config_name: ret_env_config})


T = TypeVar('T')

__SCONFIG_SECRET__ = '__sconfig_secret__'
__SCONFIG_ENV_OVERRIDE_NAME__ = '__sconfig_env_override_name__'


def secret(type_: Type[T]) -> Type[T]:
    new_type = NewType(f'secret_{type_.__name__}', type_)
    setattr(new_type, __SCONFIG_SECRET__, True)
    return new_type


def env(override_name, type_: Type[T]) -> Type[T]:
    new_type = NewType(f'secret_{type_.__name__}', type_)
    setattr(new_type, __SCONFIG_ENV_OVERRIDE_NAME__, override_name)
    return new_type


def _attrs(obj: Any) -> Dict[str, Any]:
    ret = {}
    for attr_name in dir(obj):
        if _has_lower(attr_name) or attr_name.startswith('_'):
            continue
        ret[attr_name] = getattr(obj, attr_name)
    return ret


def _hasattr_r(obj: Any, attr: str) -> bool:
    if hasattr(obj, attr):
        return True
    if hasattr(obj, '__supertype__'):
        return _hasattr_r(obj.__supertype__, attr)
    return False


def _getattr_r(obj: Any, attr: str, default):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    if hasattr(obj, '__supertype__'):
        return _getattr_r(obj.__supertype__, attr, default)
    return default


def _has_lower(s: str) -> bool:
    for c in s:
        if c.islower():
            return True
    return False


def _to_env_name(config_name, property_name):
    return f'{_to_env_config_name(config_name)}_{property_name.upper()}'


def _to_env_config_name(config_name: str) -> str:
    return uppercase(snakecase(config_name))
