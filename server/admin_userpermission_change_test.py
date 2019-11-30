'''
This is a test file to test user change permission
'''

import pytest
from error_handle import AccessError, ValueErr
from auths import admin_userpermission_change, auth_register
from iter3 import get_user_from_token, reset_data, get_perm, get_data

ADMIN = 2
OWNER = 1
MEMBER = 3

def test_admin_userpermission_change_bad1():
    '''
    invalid user id
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")

    owner_token = owner['token']
    get_user_from_token(owner_token)

    with pytest.raises(ValueErr):
        admin_userpermission_change(owner_token, 2, 4)

    print("=========pass test1 : invalid u id")


def test_admin_userpermission_change_bad2():
    '''
    user cannot change permission for himself
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")

    owner_token = owner['token']
    get_user_from_token(owner_token)

    with pytest.raises(ValueErr):
        admin_userpermission_change(owner_token, 2, 0)
    print("=========pass test2 : user cannot change permission for himself")


def test_admin_userpermission_change_bad3():
    '''
    invalid permission id
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")
    owner_token = owner['token']
    get_user_from_token(owner_token)

    with pytest.raises(ValueErr):
        admin_userpermission_change(owner_token, 4, 1)
    print("=========pass test3 : invalid permission id")


def test_admin_userpermission_change_bad4():
    '''
    user do not have permission
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    member1 = auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")

    member1_token1 = member1['token']
    admin_userpermission_change(owner['token'], 2, 1)

    with pytest.raises(ValueErr):
        admin_userpermission_change(member1_token1, 3, 1)

    print("=========pass test4 : dont have the permission")


def test_admin_userpermission_change_bad5():
    '''
    user do not have permission
    '''
    reset_data()
    auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    member2 = auth_register("1234567", "un", "sw", email="unswr@gmail.com")

    member2_token = member2['token']

    with pytest.raises(AccessError):
        admin_userpermission_change(member2_token, 2, 1)
    print("=========pass test5 : dont have the permission")


def test_admin_userpermission_change_bad6():
    '''
    can not change owner permission
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    member1 = auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")


    admin_userpermission_change(owner['token'], 2, 1)
    with pytest.raises(AccessError):
        admin_userpermission_change(member1['token'], 2, 0)

    print("=========pass test6 : cant change owner permission")


def test_admin_userpermission_change_bad7():
    '''
    cant change permission to owner
    '''
    reset_data()
    owner = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    member1 = auth_register("1234567", "un", "sw", email="unsww@gmail.com")
    auth_register("1234567", "un", "sw", email="unswr@gmail.com")

    admin_userpermission_change(owner['token'], 2, 1)
    with pytest.raises(AccessError):
        admin_userpermission_change(member1['token'], 1, 2)

    print("=========pass test7 : cant change permission to owner")


def test_admin_userpermission_change_good1():
    '''
    change permission from member to adim
    '''
    reset_data()
    owner = auth_register("1234567", "un1", "sw", email="unsw@gmail.com")
    member1 = auth_register("1234567", "un2", "sw", email="unsww@gmail.com")

    admin_userpermission_change(owner['token'], ADMIN, member1['u_id'])

    data = get_data()
    assert get_perm(member1['u_id'], data) == ADMIN
    assert get_perm(owner['u_id'], data) == OWNER

    print("=========pass test8 : change permission from member to adim")

def test_admin_userpermission_change_good2():
    '''
    change permission from member to adim
    '''
    reset_data()
    owner = auth_register("1234567", "un3", "sw", email="unsw@gmail.com")
    member1 = auth_register("1234567", "un4", "sw", email="unsww@gmail.com")

    admin_userpermission_change(owner['token'], OWNER, member1['u_id'])

    data = get_data()
    assert get_perm(member1['u_id'], data) == OWNER
    assert get_perm(owner['u_id'], data) == OWNER

    print("=========pass test9 : change permission from member to owner")

def test_admin_userpermission_change_good3():
    '''
    change permission from owner to member
    '''
    reset_data()
    o_owner = auth_register("1234567", "un3", "sw", email="unsw@gmail.com")
    n_owner = auth_register("1234567", "un4", "sw", email="unsww@gmail.com")

    admin_userpermission_change(o_owner['token'], OWNER, n_owner['u_id'])
    admin_userpermission_change(n_owner['token'], MEMBER, o_owner['u_id'])


    data = get_data()
    assert get_perm(o_owner['u_id'], data) == MEMBER
    print("=========pass test8 : change permission from owner to member")
