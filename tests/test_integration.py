from sconfig import configure, secret, _attrs, _to_env_name


def test_integration(mocker):
    _new_os_environ = {'INTEGRATION_NAME': 'Jane'}
    mocker.patch('os.environ', new=_new_os_environ)

    class Integration:
        name = 'John'
        secret_key: secret(str) = 'very secret key'

    dumps = configure(Integration)

    assert Integration.name == 'Jane'
    assert dumps == f"""* Simple Config - Integration
    name = {Integration.name}
    secret_key = [SECRET]"""


def test_attrs():
    class Person:
        name = 'John'
        age = 21

    # noinspection PyProtectedMember
    assert _attrs(Person) == dict(name='John', age=21)


def test_env_name():
    # noinspection PyProtectedMember
    assert _to_env_name('Person', 'name') == 'PERSON_NAME'
