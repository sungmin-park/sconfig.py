import os

# noinspection PyProtectedMember
from sconfig import configure, secret, _attrs, _to_env_name, _has_lower, env, _to_env_config_name


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

    dumps = configure(Integration)

    assert Integration.FIRST_NAME == 'Jane'
    assert Integration.LAST_NAME == 'Roe'
    assert Integration.SECRET_KEY == 'very secret key'
    assert dumps == f"""[Integration]
FIRST_NAME = "{Integration.FIRST_NAME}"
LAST_NAME = "{Integration.LAST_NAME}"
OVERRIDE = "CUSTOM"
SECRET_KEY = "[SECRET]"

[INTEGRATION]
INTEGRATION_FIRST_NAME = "{Integration.FIRST_NAME}"
INTEGRATION_LAST_NAME = "{Integration.LAST_NAME}"
CUSTOM_OVERRIDE = "CUSTOM"
INTEGRATION_SECRET_KEY = "[SECRET]"
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
