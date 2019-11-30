#pylint: disable-msg=too-many-function-args
'''
This file tests for the function user_profile_sethandle
'''
import pytest
from new_profile import user_profile_sethandle, user_profile
from auths import auth_register
from iter3 import reset_data
from error_handle import AccessError, ValueErr


def test_user_profile_sethandle1():
    '''
    This function tests for setting a valid handle
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_sethandle(token, 'MichelleMM')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['handle_str']) == 'michellemm'


def test_user_profile_sethandle2():
    '''
    This function tests for setting a valid handle with symbols in
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_sethandle(token, 'SallyHandle^%^*')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['handle_str']) == 'sallyhandle^%^*'


def test_user_profile_sethandle3():
    '''
    This function tests for setting a valid handle with space
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_sethandle(token, 'Sally Handle')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['handle_str']) == 'sally handle'


def test_user_profile_sethandle4():
    '''
    This function tests for setting a valid handle with numbers
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_sethandle(token, 'Sally1122Handle')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['handle_str']) == 'sally1122handle'


def test_user_profile_sethandle5():
    '''
    This function tests for setting an invalid handle with more than 20 characters
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr):
        user_profile_sethandle(token, 'S'*21)

def test_user_profile_sethandle6():
    '''
    This function tests for setting an invalid handle with less than 3 characters
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr):
        user_profile_sethandle(token, 'ss')

# invalid token
def test_user_profile_sethandle7():
    '''
    This function tests for user with invalid token
    '''
    reset_data()
    _ = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    with pytest.raises(AccessError):
        user_profile_sethandle('invalidtoken', 'sssss')

def test_user_profile_sethandle8():
    '''
    This function tests for setting an invalid handle which already exists
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    _ = auth_register('12345678', 'Vivian', 'SSS', email='lalala@gmail.com')

    with pytest.raises(ValueErr):
        user_profile_sethandle(token, 'VivianSSS')
