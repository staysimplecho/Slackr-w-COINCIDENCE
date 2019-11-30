'''
This file is to test different cases for auth_login
'''
import pytest
from error_handle import ValueErr
from auths import auth_register
from auths import auth_login
from iter3 import reset_data

def test_auth_login_bad1():
    '''
    email entered is not valid
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_login("1234sasa", email="unsw@")
    print("===========passed test2==========: invalid email")


def test_auth_login1():
    '''
    matches the right u_id
    '''
    reset_data()
    user = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    dict1 = auth_login('1234567', email='unsw@gmail.com')

    assert user['u_id'] == dict1['u_id']
    print("===========passed test3==========: same u_id")


def test_auth_login_bad3():
    '''
    wrong password
    '''
    reset_data()
    auth_register("1234567", "un", "sw", email="unsw@gmail.com")

    with pytest.raises(ValueErr):
        auth_login("1234sasa", email="unsw@gmail.com")
    print("===========passed test3==========: wrong password")


def test_auth_login_bad4():
    '''
    email not registered which is invalid
    '''
    reset_data()

    with pytest.raises(ValueErr):
        auth_login("1234sasa", email="unsw@gmail.com")
    print("===========passed test4==========: email invalid")
