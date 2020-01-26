import sconfig


def test_integration(mocker):
    _new_os_environ = {'INTEGRATION_NAME': 'Jane'}
    mocker.patch('os.environ', new=_new_os_environ)

    class Integration:
        name = 'John'

    dumps = sconfig.sconfig(Integration)

    assert Integration.name == 'Jane'
    assert dumps == f"""* Simple Config - Integration
    name = {Integration.name}"""


def test_attrs():
    class Person:
        name = 'John'
        age = 21

    # noinspection PyProtectedMember
    assert sconfig._attrs(Person) == dict(name='John', age=21)


def test_env_name():
    # noinspection PyProtectedMember
    assert sconfig._to_env_name('Person', 'name') == 'PERSON_NAME'
