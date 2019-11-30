#pylint: disable-msg=too-many-function-args
"""
This file tests for function 'user_profile_test'
"""

import pytest
from error_handle import AccessError, ValueErr
from new_profile import user_profile
from auths import auth_register
from iter3 import reset_data

# valid user
def test1_valid_user():
    """
    This test shows a valid case where user info is successfully returned
    """
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token = user['token']
    u_id = user['u_id']
    return_user_info = user_profile(token, u_id)
    assert return_user_info['email'] == 'unsw@gmail.com'
    assert return_user_info['name_first'] == 'un'
    assert return_user_info['name_last'] == 'sw'
    assert return_user_info['handle_str'] == 'unsw'

    #test the handle generator
    user1 = auth_register("1234567", "un", "sw", email="unsw1@gmail.com")
    user_info = user_profile(user1['token'], user1['u_id'])
    assert user_info['handle_str'] == 'unsw0'

    user2 = auth_register("1234567", "un", "sw", email="unsw12@gmail.com")
    user_info = user_profile(user2['token'], user2['u_id'])
    assert user_info['handle_str'] == 'unsw01'

# invalid user with non existent id
def test2_invalid_user_no_uid():
    """
    This test shows an invalid cases where user inputing invalid id
    """
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token = user['token']
    invalid_uid = 8
    with pytest.raises(ValueErr):
        _ = user_profile(token, invalid_uid)

# invalid user with invalid token
def test3_invalid_user_wrong_token():
    """
    This test shows an invalid cases where the given token is invalid
    """
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    invalid_token = '333'
    u_id = user['u_id']
    with pytest.raises(AccessError):
        _ = user_profile(invalid_token, u_id)
