#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args
'''
This is a test file for message sendlater
'''

from time import sleep
from datetime import datetime, timedelta, timezone
import pytest
from messages import message_sendlater
from messages import search_message
from channels import channels_create
from auths import auth_register
from iter3 import reset_data
from error_handle import AccessError, ValueErr

STRING = 'a' * 1200

def test_message_sendlater0():
    '''
    token not belongs to any user
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    auth_register("123eff45", "xxx", "yyyy", email="hwp@gmail.com")
    channel1 = channels_create(user1['token'], "channel01", True)

    with pytest.raises(AccessError):
        message_sendlater('asdadada', channel1['channel_id'], 'hihi', 1572246165.247)

    print("===========passed test==========: message > token not belongs to any users")

#invalid channel id
def test_message_sendlater1():
    '''
    message larger than 1000 characters
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    auth_register("123eff45", "xxx", "yyyy", email="hwio@gmail.com")
    channel1 = channels_create(user1['token'], "channel01", True)

    with pytest.raises(ValueErr):
        message_sendlater(user1['token'], channel1['channel_id'], STRING,\
         1572246165.247)

    print("===========passed test==========: message > 1000characters")

def test_message_sendlater2():
    '''
    channel id is invalid
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    auth_register("123eff45", "xxx", "yyyy", email="hww@gmail.com")
    channels_create(user1['token'], "channel01", True)

    with pytest.raises(ValueErr):
        message_sendlater(user1['token'], 2, 'hihi', 1572246165.247)

    print("===========passed test==========: invalid channel id")


def test_message_sendlater3():
    '''
    timeset is in the past
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    channel1 = channels_create(user1['token'], "channel01", True)

    timer = datetime.utcnow() - timedelta(seconds=59)
    past_time = timer.replace(tzinfo=timezone.utc).timestamp()

    with pytest.raises(ValueErr):
        message_sendlater(user1['token'], channel1['channel_id'], 'hihi', past_time)

    print("===========passed test==========: timeset is in the past")

def test_message_sendlater4():
    '''
    member is not in the channel
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    user2 = auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    channel1 = channels_create(user1['token'], "channel01", True)

    timer = datetime.utcnow() + timedelta(seconds=59)
    future_time = timer.replace(tzinfo=timezone.utc).timestamp()

    with pytest.raises(AccessError):
        message_sendlater(user2['token'], channel1['channel_id'], 'hihi', future_time)

    print("===========passed test==========: member is not in the channel")

def test_message_sendlater5():
    '''
    valid sendlater for five second delay
    '''
    reset_data()
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    channel1 = channels_create(user1['token'], "channel01", True)
    token1 = user1['token']

    timer = datetime.utcnow() + timedelta(seconds=5)
    future_time = timer.replace(tzinfo=timezone.utc).timestamp()

    msg_id = message_sendlater(user1['token'], channel1['channel_id'],\
     'hihi', future_time)
    sleep(6)

    msgs = search_message(token1, 'hi')
    #test the number of msg it return
    assert len(msgs) == 1
    assert msgs[0]['message'] == 'hihi'
    assert msgs[0]['message_id'] == msg_id
    print("===========passed test==========: valid sendlater for one second delay")
