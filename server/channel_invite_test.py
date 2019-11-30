#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains five different cases built to test channel_addowner function.
"""
import pytest
from channels import channel_invite, channels_create, channel_details
from auths import auth_register
from iter3 import reset_data
from error_handle import ValueErr, AccessError

INVALID_U = 123
INVALID_C = 123

def test_channel_invite1():
    """
    CASE1: test if function with invalid user id raises error
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    token = owner['token']
    channel_id = channels_create(token, "hi", True)['channel_id']
    with pytest.raises(ValueErr):
        _ = channel_invite(token, channel_id, INVALID_U)

    print("=========pass test1 : invalid u_id========")

def test_channel_invite2():
    """
    CASE2: test if function with invalid channel id raises error
    """
    reset_data()
    user = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    u_id = user['u_id']
    with pytest.raises(ValueErr):
        channel_invite(user['token'], INVALID_C, u_id)
    print("===========pass test2 : invalid channel_id============")

def test_channel_invite3():
    """
    CASE3: test if function raise error while inviting channel member
    to become member again
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    info = channels_create(owner['token'], "hi", True)
    channel_id = info['channel_id']
    u_id = user['u_id']
    _ = channel_invite(owner['token'], channel_id, u_id)

    with pytest.raises(ValueErr):
        _ = channel_invite(owner['token'], channel_id, u_id)
    print("=========pass test3 : invite someone who is already a member of channel")

def test_channel_invite4():
    """
    CASE4: test if function raise error with authorised user is not the member of channel
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hioo@gmail.com")

    info = channels_create(owner['token'], "hi", True)
    channel_id = info['channel_id']
    u_id = user1['u_id']

    with pytest.raises(AccessError):
        _ = channel_invite(user['token'], channel_id, u_id)
    print("=========pass test4 : authorised user is not member of channel")


def test_channel_invite5():
    """
    CASE5: test if funciton works out with valid parameter by using channel_details
    to test if user being added to channel appear in member list
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    info = channels_create(owner['token'], "hi", True)
    channel_id = info['channel_id']
    u_id = user['u_id']

    _ = channel_invite(owner['token'], channel_id, u_id)
    details = channel_details(owner['token'], channel_id)

    members = [member['u_id'] for member in details['all_members']]
    assert u_id in members, "user is not on member list"

    print("=========pass test5 : valid channel_id and user_id=======")


def test_channel_invite6():
    """
    CASE6: test if funciton works out with valid parameter by using channel_details
    to test if slackr owner being added to channel appear in owner list and member list
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    owner_c = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    info = channels_create(owner_c['token'], "hi", True)
    channel_id = info['channel_id']
    u_id = owner['u_id']

    _ = channel_invite(owner_c['token'], channel_id, u_id)
    details = channel_details(owner['token'], channel_id)

    members = [member['u_id'] for member in details['all_members']]
    owners = [o['u_id'] for o in details['owner_members']]
    assert u_id in members, "user is not on member list"
    assert u_id in owners, "user is not on owner list"

    print("=========pass test6 : invite slackr owner=======")
