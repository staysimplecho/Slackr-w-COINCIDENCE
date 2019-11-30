'''
this file is to test password_reset_reset
'''

import pytest
from error_handle import ValueErr
from auths import auth_register, passwordreset_request, passwordreset_reset
from iter3 import reset_data

# it's not worth testing for successful case

def test_auth_passwordreset_reset_bad1():
    '''
    invalid reset code
    '''
    reset_data()
    auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    with pytest.raises(ValueErr):
        passwordreset_reset("dsadasd", 1234)


def test_auth_passwordreset_reset_bad2():
    '''
    invalid password only 4 character
    '''
    reset_data()
    auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    passwordreset_request("unsw@gmail.com")
    with pytest.raises(ValueErr):
        passwordreset_reset("01qw", "ejspqi")
