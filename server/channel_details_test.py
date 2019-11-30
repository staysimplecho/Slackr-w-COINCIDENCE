#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains three different cases built to test channel_details function.
"""
import pytest
from channels import channel_join, channels_create, channel_details
from auths import auth_register
from iter3 import reset_data
from error_handle import ValueErr, AccessError

INVALID_C = 111222

def test_channel_details1():
    """
    CASE1: test if function returns error when using unexisted channel id
    """
    reset_data()
    user = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_details(user['token'], INVALID_C)
    print("======pass test1 : invalid channel_id=====")

def test_channel_details2():
    """
    CASE2: test if function works out when it only has one owner member
    after calling channel_create function
    to create a channel only has a owner.
    Test asserts if the returned dictionary is not expected.
    """
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)['channel_id']
    channel_id = channel

    response = channel_details(owner['token'], channel_id)

    assert response['name'] == "hi", "Name error"
    expected1 = [
        {
            'u_id' : owner['u_id'],
            'name_first': "xxx",
            'name_last': "yyyy",
            'profile_img_url': None
        }
    ]
    expected2 = [
        {
            'u_id' : owner['u_id'],
            'name_first': "xxx",
            'name_last': "yyyy",
            'profile_img_url': None
        }
    ]
    assert response['owner_members'] == expected1, "owner_memeber error_handle"
    assert response['all_members'] == expected2, "all_memeber error_handle"

    print("===========pass test2 : channel only has owner==========")

def test_channel_details3():
    """
    CASE3: test if function works out by using channel_create and
    channel_join functions to have multiple channel members in channel.
    Function assert if owner is not on member list or owner list, member appears
    on owner list or not on member list.
    """
    reset_data()
    owner = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    user = auth_register("123eff45", "first", "last", email="hii@gmail.com")
    channel_id = channels_create(owner['token'], "hi", True)['channel_id']

    channel_join(user['token'], channel_id) #join user to channel
    details = channel_details(user['token'], channel_id)

    assert details['name'] == "hi", "Name error"
    owners = [owner['u_id'] for owner in details['owner_members']]
    members = [member['u_id'] for member in details['all_members']]
    assert owner['u_id'] in owners, "owner is not on owner_list"
    assert user['u_id'] in members, "user is not on member_list"
    assert owner['u_id'] in members, "owner is not on member_list"
    assert user['u_id'] not in owners, "user is on owner_list"


    print("=========pass test3 : valid channel and its members==========")

def test_channel_messages4():
    '''
    user is not a member of a private channel
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", False)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError):
        channel_details(user['token'], channel_id)
    print("======pass test4 : an authorised user is not a memeber of the private channel")
