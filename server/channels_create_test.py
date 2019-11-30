#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains three different cases built to test channel_create function.
"""
import pytest
from auths import auth_register
from channels import channels_create
from error_handle import ValueErr
from iter3 import reset_data, get_data

OVER = "1324567654347654567898888665543465677889"

def test_channels_create1():
    """
    CASE1: test if function raises error when using overflow channel name
    """
    reset_data()
    user1 = auth_register("123eff45", "first", "last", email="hi@gmail.com")

    with pytest.raises(ValueErr):
        channels_create(user1['token'], OVER, True)

def test_channels_create2():
    """
    CASE2: test if function works out with valid parameter
    when creating public channel
    """
    reset_data()
    user1 = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    channel_id = channels_create(user1['token'], "channel1", True)['channel_id']
    data = get_data()
    channels = [channel.channel_id for channel in data['channels']]
    assert channel_id in channels
    print("===========pass test2: public channel===========")

def test_channels_create3():
    """
    CASE3: test if function works out with valid parameter
    when creating private channel
    """
    reset_data()
    user1 = auth_register("123eff45", "first", "last", email="hi@gmail.com")
    channel_id = channels_create(user1['token'], "channel1", False)['channel_id']
    data = get_data()
    channels = [channel.channel_id for channel in data['channels']]
    assert channel_id in channels
    print("===========pass test3: private channel===========")
