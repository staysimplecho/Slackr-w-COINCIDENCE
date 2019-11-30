#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains three different cases built to test channel_list function.
"""

from channels import channels_create, channel_join, channels_list
from auths import auth_register
from iter3 import reset_data


def test_channel_list1():
    """
    CASE1; test if function works out when there is only
    a channle exists
    """
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel1_1 = channels_create(owner1['token'], "channel1", True)['channel_id']
    channel_join(user1['token'], channel1_1)
    channel_list1 = channels_list(user1['token'])
    channels = [channel['channel_id'] for channel in channel_list1]
    assert channels == [channel1_1]
    print("=========pass test1 : only one channel in channel_list========")

def test_channel_list2():
    """
    CASE2: test if function works out by using multiple known channel_ids
    """
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user2 = auth_register("123eff45", "xxx", "yyyy", email="hie@gmail.com")
    owner1 = auth_register("123eff45", "xxx", "yyyy", email="hri@gmail.com")
    owner2 = auth_register("123eff45", "xxx", "yyyy", email="hiw@gmail.com")
    channel1_1 = channels_create(owner1['token'], "channel1", True)['channel_id']
    channel2_2 = channels_create(owner2['token'], "channel2", True)['channel_id']
    channel_join(user1['token'], channel1_1)
    channel_join(user1['token'], channel2_2)
    channel_join(user2['token'], channel1_1)
    channel_join(user2['token'], channel2_2)

    channel_list1 = channels_list(user1['token'])
    channels1 = [channel['channel_id'] for channel in channel_list1]
    channel_list2 = channels_list(user2['token'])
    channels2 = [channel['channel_id'] for channel in channel_list2]

    assert (channel1_1 in channels1 and channel2_2 in channels1 and
            channel1_1 in channels2 and channel2_2 in channels2)
    print("=============pass test2 : channels and users=============")


def test_channel_list3():
    """
    CASE3: test if function return empty list if
    user has not join any channel
    """
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user2 = auth_register("123eff45", "xxx", "yyyy", email="ihi@gmail.com")
    _ = channels_create(user2['token'], "channel1", True)['channel_id']
    assert channels_list(user1['token']) == []
    print("=============pass test3 : user didn't join in channels=============")
