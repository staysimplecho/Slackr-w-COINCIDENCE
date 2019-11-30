#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains five different cases built to test channel_removeowner function.
"""
import pytest
from error_handle import AccessError, ValueErr
from channels import channels_create, channel_details
from channels import channel_addowner, channel_removeowner
from auths import auth_register
from iter3 import reset_data

INVALID_C = 111

def test_channel_removeowner1():
    """
    CASE1: test if function raise error when using a unexisted channel id
    """
    reset_data()
    user = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_removeowner(user['token'], INVALID_C, user['u_id'])
    print("========pass test1 : unexisted channel_id=======")

def test_channel_removeowner2():
    """
    CASE2: test if function raise error when remove user who is not owner of channel
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    user = auth_register("123eff45", "first", "last", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", True)['channel_id']

    with pytest.raises(ValueErr):
        channel_removeowner(owner['token'], channel, user['u_id'])
    print("=========pass test2 : remove someone who is not owner of that channel")

def test_channel_removeowner3():
    """
    CASE3: test if function raise error when try to remove only owner in channel
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)['channel_id']

    with pytest.raises(AccessError):
        channel_removeowner(owner['token'], channel, owner['u_id'])
    print("=======pass test3 : remove the only owner in channel==========")

def test_channel_removeowner4():
    """
    CASE4: test if function works out with valid parameter
    by using channel details to test if owner has been removed
    is not in owner list of channel but still in member list
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hello@gmail.com")
    user1 = auth_register("123eff45", "fi", "last", email="hii@gmail.com")

    channel = channels_create(user1['token'], "hi", True)['channel_id']
    channel_addowner(user1['token'], channel, owner['u_id']) #add user as owner
    channel_removeowner(owner['token'], channel, user1['u_id']) #remove original owner

    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert user1['u_id'] not in owners, "user is still in owner list"
    assert user1['u_id'] in members, "user should still in member list"
    print("=======pass test4 : owner remove other owner=====")

def test_channel_removeowner5():
    """
    CASE5: test if function raises error when authorised user who
    is not the owner try to remove channel owner
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    user1 = auth_register("123eff45", "first", "last", email="hp@gmail.com")

    channel = channels_create(owner['token'], "hi", True)['channel_id']
    channel_addowner(owner['token'], channel, user1['u_id']) #add other owner to avoid other error

    user = auth_register("123eff45", "first", "last", email="hii@gmail.com")
    with pytest.raises(AccessError):
        channel_removeowner(user['token'], channel, owner['u_id'])

    print("=========pass test5 : authorised user is not the owner of channel===========")

def test_channel_removeowner6():
    """
    CASE5: test if function raises error when authorised user \
    whose permission_id is 3 tried to remove a channel owner with permission_id 1/2
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    user1 = auth_register("123eff45", "first", "last", email="hp@gmail.com")

    channel = channels_create(user1['token'], "hi", True)['channel_id']
    channel_addowner(user1['token'], channel, owner['u_id'])

    with pytest.raises(AccessError):
        channel_removeowner(user1['token'], channel, owner['u_id'])

    print("=========pass test5 : authorised user tried to remove slackr owner===========")
