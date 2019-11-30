#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains three different cases built to test standup_active function.
"""
import time
import pytest
from error_handle import ValueErr
from channels import channels_create
from auths import auth_register
from iter3 import reset_data
from standup import standup_start, standup_active

def test_standup_acitve1():
    """
    standup acitve with channel id that doesn't exist
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']

    with pytest.raises(ValueErr):
        standup_active(token1, 1)

def test_standup_acitve2():
    """
    test standup stage just after creating channel
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']

    assert standup_active(token1, channel1_1) == (False, None)

def test_standup_acitve3():
    """
    test if standup stage is active after calling standup_start function with length 3s
    and if is deacive 4s later
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token1 = user1['token']
    channel1_1 = channels_create(user1['token'], "channel1", True)['channel_id']
    _ = standup_start(token1, channel1_1, 3)

    assert standup_active(token1, channel1_1)[0] is (True)
    time.sleep(4)
    assert standup_active(token1, channel1_1) == (False, None)
