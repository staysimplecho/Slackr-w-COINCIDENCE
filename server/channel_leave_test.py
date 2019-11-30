#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains four different cases built to test channel_leave function.
"""

import pytest
from channels import channel_leave, channels_create, channel_details, channel_join, channel_addowner
from auths import auth_register
from iter3 import reset_data
from error_handle import AccessError, ValueErr

INVALID_C = 111

def test_channel_leave1():
    """
    CASE1: test if function with unexisted channel id raise error
    """
    reset_data()
    user = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_leave(user['token'], INVALID_C)
    print("========pass test1 : unexisted channel_id=======")

def test_channel_leave2():
    """
    CASE2: test if function raises error when the only owner try to leave channel
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError):
        channel_leave(owner['token'], channel_id) #leave

    print("=========pass test2 : only owner leave channel=======")

def test_channel_leave3():
    """
    CASE3: test if function works out with valide parameter
    by using channel_details functions to test if user is
    not existed in channel member list
    """
    reset_data()
    owner = auth_register("123000000", "hi", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    channel_join(user['token'], channel_id) #join user to channel
    channel_leave(user['token'], channel_id) #leave
    details = channel_details(owner['token'], channel_id)
    members = [member['u_id'] for member in details['all_members']]
    assert user['u_id'] not in members
    print("=========pass test3 : member left channel=======")

def test_channel_leave4():
    """
    CASE4: test if function works out when channel owner leave channel
    by using channel_details function to test if "owner" is not
    in member list as well as owner list
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    channel_addowner(owner['token'], channel_id, owner1['u_id']) #add owner
    channel_leave(owner1['token'], channel_id) #leave

    details = channel_details(owner['token'], channel_id)
    owners = [owner['u_id'] for owner in details['owner_members']]
    assert (owner['u_id'] in owners) and (owner1['u_id'] not in owners)
    print("=========pass test4 : one of the owners left=======")
