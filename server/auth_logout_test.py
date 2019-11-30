'''
This file is to test different cases for auth_logout
'''

from auths import auth_logout, auth_register
from iter3 import reset_data

def test_successful_logout():
    '''
    the user is able to successfully logout
    '''
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    user_token = user['token']
    assert auth_logout(user_token)


def test_auth_logout_bad():
    '''
    once the user logout, he cannot lougout again
    '''
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    user_token = user['token']
    auth_logout(user_token)
    assert not auth_logout(user_token)
