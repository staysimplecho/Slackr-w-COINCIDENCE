'''
this file is to test password_reset_request
'''
import pytest
from error_handle import ValueErr
from iter3 import reset_data
from auths import auth_register, passwordreset_request, passwordreset_reset


#invalid reset code
def test_auth_passwordreset_reset_bad1():
    '''
    test for invalid reset code
    '''
    reset_data()
    auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    passwordreset_request("unsw@gmail.com")

    with pytest.raises(ValueErr):
        passwordreset_reset("dsadasd", 1234)
    print("===========passed test==========: invalid reset code")
