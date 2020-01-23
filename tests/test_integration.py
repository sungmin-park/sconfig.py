import sconfig


def test_integration(mocker):
    _new_os_environ = {'CONFIG_NAME': 'Jane'}
    mocker.patch('os.environ', new=_new_os_environ)

    class Config:
        name = 'John'

    sconfig.sconfig(Config)

    assert Config.name == 'Jane'


def test_attrs():
    class Person:
        name = 'John'
        age = 21

    # noinspection PyProtectedMember
    assert sconfig._attrs(Person) == dict(name='John', age=21)


def test_env_name():
    # noinspection PyProtectedMember
    assert sconfig._to_env_name('Person', 'name') == 'PERSON_NAME'
