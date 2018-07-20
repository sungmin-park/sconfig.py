from unittest.mock import patch

from sconfig import configure

FIRST_NAME = 'John'
LAST_NAME = 'Doe'
AGE = 22
HAS_JOB = False

_new_os_environ = {'FIRST_NAME': 'Jone', 'AGE': '30', 'HAS_JOB': 'true'}


@patch('os.environ', new=_new_os_environ)
def test_integration():
    configure(__name__)

    # check module variables are changed
    assert FIRST_NAME == 'Jone'
    assert AGE == 30
    assert HAS_JOB is True

    # check os.environ missing values are set
    assert _new_os_environ['LAST_NAME'] == 'Doe'
