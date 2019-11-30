#pylint: disable-msg=too-many-function-args
'''
This file tests the function user_profile_setemail
'''
import pytest
from new_profile import user_profile_setemail, user_profile
from auths import auth_register
from iter3 import reset_data
from error_handle import AccessError, ValueErr

def test_user_profile_setemail1():
    '''
    This test checks for a valid change of email (different prefix)
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_setemail(token, email='Sally12138@gamil.com')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['email']) == 'Sally12138@gamil.com'

def test_user_profile_setemail2():
    '''
    This test checks for a valid change of email (different suffix)
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_setemail(token, email='Sally@ourearth.org')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['email']) == 'Sally@ourearth.org'

def test_user_profile_setemail3():
    '''
    This test checks for a valid change of email with mixed numbers and\
    letters (lower and upper cases) present in the prefix
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    u_id = user_dic['u_id']
    user_profile_setemail(token, email='SallyHSO12138@gamil.com')
    user_info_dic = user_profile(token, u_id)
    assert(user_info_dic['email']) == 'SallyHSO12138@gamil.com'

def test_user_profile_setemail4():
    '''
    This test checks for an invalid change of email with unallowed symbols
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr, match=r"Invalid Email."):
        user_profile_setemail(token, email='Sally&&#12138@gamil.com')

def test_user_profile_setemail5():
    '''
    This test checks for an invalid change of email with spacess
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr, match=r"Invalid Email."):
        user_profile_setemail(token, email='Sally 12138gamil.com')

def test_user_profile_setemail6():
    '''
    This test checks for an invalid change of email with no @
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']
    with pytest.raises(ValueErr, match=r"Invalid Email."):
        user_profile_setemail(token, email='Sally12138gmail.com')

def test_user_profile_setemail7():
    '''
    This test checks for an invalid change of email with the email being registered before
    '''
    reset_data()
    user_dic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = user_dic['token']

    user_dic = auth_register('12345678', 'Marc', 'Chee', email='Marc12138@unsw.edu.au')

    with pytest.raises(ValueErr):
        user_profile_setemail(token, email='Marc12138@unsw.edu.au')

def test_user_profile_setemail8():
    '''
    This test checks for an invalid change of email with the user holding wrong token
    '''
    reset_data()
    _ = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    invalid_token = '123'

    with pytest.raises(AccessError):
        user_profile_setemail(invalid_token, email='Marc12138@unsw.edu.au')
