# noinspection PyProtectedMember
from sconfig import configure, secret, _attrs, _to_env_name, _has_lower, env


def test_integration(mocker):
    _new_os_environ = {'INTEGRATION_NAME': 'Jane', 'CUSTOM_OVERRIDE': 'CUSTOM'}
    mocker.patch('os.environ', new=_new_os_environ)

    class Integration:
        NAME = 'John'
        OVERRIDE: env('CUSTOM_OVERRIDE', str) = 'DEFAULT'
        SECRET_KEY: secret(str) = 'very secret key'

    dumps = configure(Integration)

    assert Integration.NAME == 'Jane'
    assert Integration.SECRET_KEY == 'very secret key'
    assert dumps == f"""* Simple Config - Integration
    NAME = {Integration.NAME}
    OVERRIDE = CUSTOM
    SECRET_KEY = [SECRET]"""


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
    assert _to_env_name('Person', 'NAME') == 'PERSON_NAME'
