#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains four different cases built to test standup_start function.
"""

from datetime import timedelta, datetime, timezone
from time import sleep
import pytest
from error_handle import AccessError, ValueErr
from channels import channels_create
from auths import auth_register
from iter3 import reset_data
from standup import standup_start
# from messages import search_message

STANDUP_LEN = 5
WAIT_LEN = 7

def test_standup_start1():
    """
    test if function return approx finish time if standup in an existing channel
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    value = standup_start(token1, channel1_1, STANDUP_LEN)
    timer = datetime.utcnow()
    timer = timer + timedelta(seconds=1)
    timestamp = timer.replace(tzinfo=timezone.utc).timestamp()
    sleep(WAIT_LEN)

    # msg = search_message(token1, "standup")
    # msg_id = msg[0]['message_id']
    # data = get_data()
    # index = find_channel(data['channels'], channel1_1)
    # assert msg_id in data['channels'][index].messages
    assert (value - timestamp) < STANDUP_LEN

def test_standup_start2():
    """
    test if function raise error if channel does not exist
    """
    reset_data()
    token1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")['token']
    with pytest.raises(ValueErr):
        standup_start(token1, 999, STANDUP_LEN)

def test_standup_start3():
    """
    test if funciton raises error if the user is not a member of the channel
    """
    reset_data()
    token1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")['token']
    token2 = auth_register("1234567", "un", "sw", email="unsww@gmail.com")['token']
    channel2 = channels_create(token2, "channel", True)['channel_id']
    with pytest.raises(AccessError):
        standup_start(token1, channel2, STANDUP_LEN)

def test_standup_start4():
    """
    test if function raises error if
    start "stand up" in channel which already has a active standup session
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    _ = standup_start(token1, channel1_1, STANDUP_LEN)
    sleep(STANDUP_LEN / 2)
    with pytest.raises(ValueErr):
        standup_start(token1, channel1_1, STANDUP_LEN)
    sleep(WAIT_LEN)
