from sconfig import configure, secret, _attrs, _to_env_name


def test_integration(mocker):
    _new_os_environ = {'INTEGRATION_NAME': 'Jane'}
    mocker.patch('os.environ', new=_new_os_environ)

    class Integration:
        NAME = 'John'
        SECRET_KEY: secret(str) = 'very secret key'

    dumps = configure(Integration)

    assert Integration.NAME == 'Jane'
    assert Integration.SECRET_KEY == 'very secret key'
    assert dumps == f"""* Simple Config - Integration
    NAME = {Integration.NAME}
    SECRET_KEY = [SECRET]"""


def test_attrs():
    class Person:
        NAME = 'John'
        AGE = 21

    # noinspection PyProtectedMember
    assert _attrs(Person) == dict(NAME='John', AGE=21)


def test_env_name():
    # noinspection PyProtectedMember
    assert _to_env_name('Person', 'NAME') == 'PERSON_NAME'
