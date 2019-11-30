#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains five different cases built to test channel_listall function.
"""
from channels import channels_create, channel_join, channels_listall, channel_leave, channel_invite
from auths import auth_register
from iter3 import reset_data


def test_channel_listall1():
    """
    CASE1: test if function return empty list if not any channel created
    """
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")

    assert channels_listall(user1['token']) == []
    print("======pass test1 : empty channel list==========")

def test_channel_listall2():
    """
    CASE2: test if function return correct channel name and id
    after creating a public channel
    """
    reset_data()
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")

    channel1 = channels_create(owner1['token'], "channel1", True)['channel_id']
    expected = [
        {
            "channel_id": channel1,
            "name": "channel1"
        }
    ]
    assert channels_listall(user1['token']) == expected
    print("=============pass test2 : one public channel============")


def test_channel_listall3():
    """
    CASE3: test if function return correct channel name and id
    after joinning in a private channel
    """
    reset_data()
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")

    channel1 = channels_create(owner1['token'], "channel1", False)['channel_id']
    channel_invite(owner1['token'], channel1, user1['u_id'])
    expected = [
        {
            "channel_id": channel1,
            "name": "channel1"
        }
    ]
    assert channels_listall(user1['token']) == expected
    print("=============pass test2 : one private channel============")


def test_channel_listall4():
    """
    CASE4: test if function return correct info after
    creating multiple channels, excluded private channels that the authorised user is not a member of
    """
    reset_data()
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    owner2 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    owner3 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    channel1 = channels_create(owner1['token'], "channel1", True)['channel_id']
    channel2 = channels_create(owner2['token'], "channel2", True)['channel_id']
    channels_create(owner3['token'], "channel3", False)['channel_id']
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hiii@gmail.com")

    expected = [
        {
            "channel_id": channel1,
            "name": "channel1"
        },
        {
            "channel_id": channel2,
            "name": "channel2"
        }
    ]

    assert channels_listall(user1['token']) == expected
    print("=============pass test4 : multiple channels============")

def test_channel_listall5():
    """
    CASE5: test if channel_join and channel_leave will effect the result
    of listall which shouldn't
    """
    reset_data()
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel1 = channels_create(owner1['token'], "channel1", True)['channel_id']
    expected = [
        {
            "channel_id": channel1,
            "name": "channel1"
        }
    ]
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel_join(user1['token'], channel1)
    assert channels_listall(user1['token']) == expected

    channel_leave(user1['token'], channel1)
    assert channels_listall(user1['token']) == expected

    print("=========pass test5 : test with channel_join and channel_leave============")
