#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains three different cases built to test userall function.
"""
import pytest
from error_handle import AccessError
from iter3 import reset_data
from auths import auth_register
from new_profile import users_listall

INVALID_T = "tokenunkown"

def test_invalid_token():
    """
    test if function raises error when it has invalid token
    """
    with pytest.raises(AccessError): # Invalid token
        users_listall(INVALID_T)

def test_only_one():
    """
    test if function works out with correct input
    by testing the number of user it return which should be 1
    """
    reset_data()
    # pId = 1, owner of the Slackr
    owner = auth_register("1234567", "un", "sw", email="unsw12@gmail.com")
    token_s_o = owner['token']
    users_list = users_listall(token_s_o)
    assert len(users_list) == 1

def test_more_users():
    """
    test if function works out with correct input
    by testing the number of user it return which should be ten
    """
    reset_data()
    # register 10 users
    for i in range(9):
        email = 'user_' + f'{i}' + '@gmail.com'
        first_name = 'who' + f'{i}'
        last_name = 'ever' + f'{i}'
        _ = auth_register("1234567", first_name, last_name, email=email)
    user9 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token = user9['token']
    users_list = users_listall(token)
    assert len(users_list) == 10
