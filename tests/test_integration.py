from sconfig import configure

FIRST_NAME = 'John'
LAST_NAME = 'Doe'
AGE = 22
HAS_JOB = False
MARRIED = False
APPLE_P8 = 'apple'


def test_integration(mocker):
    # mock os.environ
    _new_os_environ = {'FIRST_NAME': 'Jone', 'AGE': '30', 'HAS_JOB': 'true', 'MARRIED': 'false', 'APPLE_P8': 'banana'}
    mocker.patch('os.environ', new=_new_os_environ)

    configure(__name__)

    # check module variables are changed
    assert FIRST_NAME == 'Jone'
    assert AGE == 30
    assert HAS_JOB is True
    assert MARRIED is False
    # check numeric variables in module are applied
    assert APPLE_P8 == 'banana'

    # check os.environ missing values are set
    assert _new_os_environ['LAST_NAME'] == 'Doe'
