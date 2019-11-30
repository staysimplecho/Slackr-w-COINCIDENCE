#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains six different cases built to test standup_send function.
"""

from time import sleep
import pytest
from error_handle import AccessError, ValueErr
from standup import standup_send, standup_start
from auths import auth_register
from iter3 import reset_data
from channels import channels_create, channel_join
from messages import search_message

STANDUP_LEN = 5
WAIT_LEN = 7

def test_standup_send1():
    """
    sending a normal message to a valid channel which doesn't have active standup session
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    with pytest.raises(ValueErr):
        standup_send(token1, channel1_1, 'abc')

def test_standup_send2():
    """
    sending an empty message to a valid channel
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    user2 = auth_register("1234567", "un", "sw", email="unswq@gmail.com")
    token1 = user1['token']
    token2 = user2['token']

    channel1_1 = channels_create(token1, "channel1", True)['channel_id']
    channel_join(token2, channel1_1)
    _ = standup_start(token1, channel1_1, STANDUP_LEN)
    standup_send(token1, channel1_1, 'hi')
    standup_send(token2, channel1_1, 'hello')
    sleep(WAIT_LEN)
    assert search_message(token1, 'hi')[0]['message'] == 'unsw : hi, unsw0 : hello'

def test_standup_send3():
    """
    sending an invalid message that has over 1000 characters
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    with pytest.raises(ValueErr):
        standup_send(token1, channel1_1, 'B'*1001)

def test_standup_send4():
    """
    sending a message to a channel that the user is not in.
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    standup_start(token1, channel1_1, STANDUP_LEN)
    user2 = auth_register("1234567", "un", "sw", email="unsw1@gmail.com")
    token2 = user2['token']

    with pytest.raises(AccessError):
        standup_send(token2, channel1_1, 'abc')
    sleep(WAIT_LEN)

def test_standup_send5():
    """
    sending a normal message to a invalid channel which doesn't exist
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    with pytest.raises(ValueErr):
        standup_send(token1, 1, 'abc')
