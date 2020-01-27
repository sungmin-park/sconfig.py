import os

# noinspection PyProtectedMember
from sconfig import configure, secret, _attrs, _to_env_name, _has_lower, env, _to_env_config_name, _hasattr_r, \
    __SCONFIG_SECRET__, __SCONFIG_ENV_OVERRIDE_NAME__, _getattr_r


def test_integration(mocker):
    _new_os_environ = {
        'INTEGRATION_FIRST_NAME': 'Jane', 'CUSTOM_OVERRIDE': 'CUSTOM',
        'SCONFIG_INTEGRATION':
            os.path.join(os.path.dirname(__file__), 'test-config.toml'),
    }
    mocker.patch('os.environ', new=_new_os_environ)

    class Integration:
        FIRST_NAME = 'John'
        LAST_NAME = 'Doe'
        OVERRIDE: env('CUSTOM_OVERRIDE', str) = 'DEFAULT'
        SECRET_KEY: secret(str) = 'very secret key'
        SECRET_KEY_OVERRIDE: secret(env('', str)) = 'very secret key override'
        OVERRIDE_SECRET_KEY: env('CUSTOM_OVERRIDE_SECRET', secret(str)) = 'override very secret key'

    dumps = configure(Integration)

    assert Integration.FIRST_NAME == 'Jane'
    assert Integration.LAST_NAME == 'Roe'
    assert Integration.SECRET_KEY == 'very secret key'
    assert dumps == f"""[Integration]
FIRST_NAME = "{Integration.FIRST_NAME}"
LAST_NAME = "{Integration.LAST_NAME}"
OVERRIDE = "CUSTOM"
OVERRIDE_SECRET_KEY = "[SECRET]"
SECRET_KEY = "[SECRET]"
SECRET_KEY_OVERRIDE = "[SECRET]"

[INTEGRATION]
INTEGRATION_FIRST_NAME = "{Integration.FIRST_NAME}"
INTEGRATION_LAST_NAME = "{Integration.LAST_NAME}"
CUSTOM_OVERRIDE = "CUSTOM"
INTEGRATION_OVERRIDE_SECRET_KEY = "[SECRET]"
INTEGRATION_SECRET_KEY = "[SECRET]"
INTEGRATION_SECRET_KEY_OVERRIDE = "[SECRET]"
"""


def test_attrs():
    class Person:
        NAME = 'John'
        AGE = 21

        def not_config(self):
            pass

    assert _attrs(Person) == dict(NAME='John', AGE=21)


def test_has_lower():
    assert _has_lower('test')
    assert _has_lower('Test')
    assert not _has_lower('TEST')


def test_env_name():
    assert _to_env_name('PersonAddress', 'NAME') == 'PERSON_ADDRESS_NAME'


def test_env_config_name():
    assert _to_env_config_name('PersonAddress') == 'PERSON_ADDRESS'


def test_has_attr_r():
    assert _hasattr_r(env('', secret(str)), __SCONFIG_ENV_OVERRIDE_NAME__)
    assert _hasattr_r(env('', secret(str)), __SCONFIG_SECRET__)
    assert _hasattr_r(secret(str), __SCONFIG_ENV_OVERRIDE_NAME__) is False


def test_getattr_r():
    assert _getattr_r(env('name', str), __SCONFIG_ENV_OVERRIDE_NAME__, None) == 'name'
    assert _getattr_r(secret(env('name', str)), __SCONFIG_ENV_OVERRIDE_NAME__, None) == 'name'
    assert _getattr_r(secret(type), __SCONFIG_ENV_OVERRIDE_NAME__, None) is None
