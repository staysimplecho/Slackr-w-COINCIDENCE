#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains five different cases built to test channel_addowner function.
"""
import pytest
from error_handle import AccessError, ValueErr
from channels import channels_create, channel_details, channel_addowner, channel_join
from auths import auth_register
from iter3 import reset_data

IVALID_C = 1111333

def test_channel_addowner1():
    """
    case1: test if function with unexisted channel_id return error
    """
    reset_data()
    user = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_addowner(user['token'], IVALID_C, user['u_id'])
    print("========pass test1 : unexisted channel_id=======")

def test_channel_addowner2():
    """
    CASE2: test if function return error while making channel owner to channel owner again
    """
    reset_data()
    owner1 = auth_register("123fgeefg45", "first", "last", email="hi@gmail.com")
    owner2 = auth_register("123gffgs45", "first", "last", email="hello@gmail.com")
    channel = channels_create(owner1['token'], "hi", True)['channel_id']

    channel_addowner(owner1['token'], channel, owner2['u_id']) #add owner2 to channel_owner

    with pytest.raises(ValueErr):
        channel_addowner(owner1['token'], channel, owner2['u_id'])
    print("=========pass test2 : add someone who is already owner of that channel")

def test_channel_addowner3():
    """
    CASE3: test if funciton return error when authorised user
    who is not channel owner try to add owner to channel
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    user1 = auth_register("123eff45", "first", "last", email="hello@gmail.com")
    user2 = auth_register("123eff45", "first", "last", email="he@gmail.com")

    channel = channels_create(owner['token'], "hi", True)['channel_id']
    with pytest.raises(AccessError):
        channel_addowner(user1['token'], channel, user2['u_id'])
    print("=======pass test3 : authorised user is not an owner of the channel=========")

def test_channel_addowner4():
    """
    CASE4: test if function works out when normal user to owner by using channel_details function
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hello@gmail.com")
    channel = channels_create(owner['token'], "hi", True)['channel_id']
    user1 = auth_register("123eff45", "first", "last", email="hi@gmail.com")

    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert user1['u_id'] not in members

    channel_addowner(owner['token'], channel, user1['u_id'])
    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert (user1['u_id'] in owners) and (user1['u_id'] in members)

    print("=======pass test4 : owner add another user who\
        is not member of that channel to become owner=========")

def test_channel_addowner5():
    """
    CASE5: test if function works out when add
    chanenl member to owner by using channel_details function
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)['channel_id']
    user = auth_register("123eff45", "first", "last", email="hello@gmail.com")
    channel_join(user['token'], channel)

    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert (user['u_id'] in members) and (user['u_id'] not in owners)

    channel_addowner(owner['token'], channel, user['u_id'])
    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    assert user['u_id'] in owners

    print("=========pass test5 : member becomes owner===========")

def test_channel_addowner6():
    """
    CASE6: test if function works out when
    add slackr owner to owner by using channel_details function
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hii@gmail.com")
    owner_channel = auth_register("123eff45", "first", "last", email="hello@gmail.com")
    channel = channels_create(owner_channel['token'], "hi", True)['channel_id']

    channel_addowner(owner_channel['token'], channel, owner['u_id'])
    details = channel_details(owner['token'], channel)
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert (owner['u_id'] in owners) and (owner['u_id'] in members)

    print("=========pass test6 : add slackr owner to channel owners===========")
