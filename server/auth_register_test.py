'''
This file is to test different cases for auth_register
'''
#pylint: disable=too-many-function-args
import pytest
from error_handle import ValueErr
from iter3 import reset_data
from auths import auth_register
from new_profile import user_profile

# GLOBAL VALUE BELOW
STRING = 'dead' * 20
SEED = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
# GLOBAL VALUE ABOVE

#password <6 character
def test_auth_register_bad1():
    '''
    password <6 character
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("123q", "first", "last", email="unsw@edu.com")
    print("===========passed test==========: invalid password")


def test_auth_register_bad11():
    '''
    password == none
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("None", "first", "last", email="unsw@edu.com")
    print("===========passed test==========: invalid password")


def test_auth_register_bad2():
    '''
    firstname > 50 character
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("123qw34", STRING, "last", email="unsw@edu.com")
    print("===========passed test==========: invalid first name")


def test_auth_register_bad21():
    '''
    lastname > 50 character
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("123ewewq", 'first', STRING, email="unsw@edu.com")
    print("===========passed test==========: invalid last name")

def test_auth_register_bad22():
    '''
    firstname, lastname > 50
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("123fgqw34", STRING, STRING, email="unsw@edu.com")
    print("===========passed test==========: invalid first name")


def test_auth_register_bad4():
    '''
    invalid email
    '''
    reset_data()
    with pytest.raises(ValueErr):
        auth_register("12387qw", "first", "last", email="1234.com")
    print("===========passed test==========: invalid email")

def test_auth_register_bad5():
    '''
    email already be used
    '''
    reset_data()
    auth_register('12345678', 'first', 'last', email="unsw@123.com")
    with pytest.raises(ValueErr):
        auth_register("12345678", "first", "last", email="unsw@123.com")
    print("===========passed test==========: email already exist")


def test_auth_register_ok1():
    '''
    handle cutoff 20
    '''
    reset_data()
    user = auth_register('12345678', 'first123456789', 'last1234567',
                         email="unsw@123.com")
    u_id = user['u_id']
    token = user['token']
    details = user_profile(token, u_id)
    handle = 'first123456789' + 'last1234567'
    handle = handle[0:20]
    assert details['handle_str'] == handle
    print("===========passed test==========: handle cutoff")

# default handle already exists -- under HANDLE_LEN
def test_auth_register_ok2():
    '''
    default handle already exists
    '''
    reset_data()
    user = auth_register('12345678', 'first', 'last', email="unsw@123.com")
    u_id = user['u_id']
    token = user['token']
    details = user_profile(token, u_id)
    user1 = auth_register('12345678', 'first', 'last', email="diff@123.com")
    u_id1 = user1['u_id']
    token1 = user1['token']
    details1 = user_profile(token1, u_id1)
    assert details1['handle_str'] == details['handle_str'] + '0'
    print("===========passed test==========: email realdy exist")

def test_auth_register_ok3():
    '''
    default handle already exists -- exceed HANDLE_LEN
    '''
    reset_data()
    user = auth_register('12345678', 'firstfirst', 'llastllast', email="unsw@123.com")
    u_id = user['u_id']
    token = user['token']
    details = user_profile(token, u_id)
    user1 = auth_register('12345678', 'firstfirst', 'llastllast', email="diff@123.com")
    u_id1 = user1['u_id']
    token1 = user1['token']
    details1 = user_profile(token1, u_id1)
    assert details1['handle_str'] == details['handle_str'][0:19] + '0'
    print("===========passed test==========: email realdy exist")
