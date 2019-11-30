#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains four different cases built to test channel_join function.
"""
import pytest
from error_handle import AccessError, ValueErr
from channels import channels_create, channel_details, channel_join
from auths import auth_register
from iter3 import reset_data

def test_channel_join1():
    """
    CASE1: test if function with unexisted channel id raise error
    """
    reset_data()
    user = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_join(user['token'], "111111123")
    print("========pass test1 : unexisted channel_id=======")

def test_channel_join2():
    """
    CASE2: test if function raise error when authorised user who is not slackr admin
    try to join private channel
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", False) #create private channel
    channel_id = channel['channel_id']

    with pytest.raises(AccessError):
        channel_join(user['token'], channel_id)
    print("========pass test2 : private channel=============")

def test_channel_join3():
    """
    CASE3: test if funtions works out with valid parameter by using
    channel_details function to test if user in member list
    """
    reset_data()
    owner = auth_register("halooooo", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    channel_join(user['token'], channel_id)
    details = channel_details(user['token'], channel_id)
    members = [member['u_id'] for member in details['all_members']]
    assert user['u_id'] in members

    print("=========pass test3 : public channel===========")

def test_channel_join4():
    """
    CASE4: test if funtions works out with slackr owner by using
    channel_details function to test if slackr owner is in
    owner list and member list after joining that channel
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    owner_c = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner_c['token'], "hi", True)
    channel_id = channel['channel_id']

    channel_join(owner['token'], channel_id)
    u_id = owner['u_id']
    details = channel_details(owner['token'], channel_id)
    members = [member['u_id'] for member in details['all_members']]
    owners = [o['u_id'] for o in details['owner_members']]
    assert u_id in members, "user is not on member list"
    assert u_id in owners, "user is not on owner list"

    print("=========pass test4 : private channel and slackr admin===========")
