#pylint: disable-msg=too-many-function-args
'''
This file tests the function user_profile_setname
'''
import pytest
from new_profile import user_profile_setname, user_profile
from auths import auth_register
from iter3 import reset_data
from error_handle import AccessError, ValueErr

def test_user_profile_setname1():
    '''
    This test checks for valid change of name
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_setname(token, 'Michelle', 'MMM')
    user_dic_reset = user_profile(token, u_id)
    assert user_dic_reset['name_first'] == 'Michelle'
    assert user_dic_reset['name_last'] == 'MMM'


def test_user_profile_setname2():
    '''
    This test checks for a valid change of name with symbols
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_setname(token, 'Sally&^', 'Smiths$$')
    user_dic_reset = user_profile(token, u_id)
    assert user_dic_reset['name_first'] == 'Sally&^'
    assert user_dic_reset['name_last'] == 'Smiths$$'


def test_user_profile_setname3():
    '''
    This test checks for an invalid change of name with spaces
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr):
        user_profile_setname(token, 'Sall y', 'Smi t hs')


def test_user_profile_setname4():
    '''
    This test checks for an invalid change of name with user having more than 50 characters
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    first_n = 's' * 100
    last_n = 'm' * 100
    with pytest.raises(ValueErr):
        user_profile_setname(token, first_n, last_n)


def test_user_profile_setname5():
    '''
    This test checks for an invalid change of name with user having empty firstname/lastname
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr):
        user_profile_setname(token, '\n', '\n')

def test_user_profile_setname6():
    '''
    This test checks for an invalid change of name with the user holding wrong token
    '''
    reset_data()
    with pytest.raises(AccessError):
        user_profile_setname('Invalidtoken', 'name1', 'name2')
