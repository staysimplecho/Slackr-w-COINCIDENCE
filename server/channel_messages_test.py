#pylint: disable-msg=too-many-function-args
"""
This file is to test different cases for channel messages
"""
import pytest
from error_handle import AccessError, ValueErr
from channels import channels_create, channel_join, channel_messages
from messages import message_send, message_react
from auths import auth_register
from iter3 import reset_data

def test_channel_messages1():
    '''
    The channel id is not valid
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    with pytest.raises(ValueErr):
        channel_messages(owner['token'], "1231111", 1)
    print("=======pass test1 : unexisted channel=========")


def test_channel_messages2():
    '''
    start point bigger than the total amount of messages
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    with pytest.raises(ValueErr):
        channel_messages(owner['token'], channel_id, 1) #one is greater than 0
    print("========pass test2 : start point larger than number of messages")


def test_channel_messages3():
    '''
    user is not a member of a private channel
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", False)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError):
        channel_messages(user['token'], channel_id, 0)
    print("======pass test3 : an authorised user is not a memeber of the private channel")


def test_channel_messages4():
    '''
    message less than 50
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']
    channel_join(user['token'], channel_id)

    i = 0
    while i < 5:
        i = i + 1
        #mid is the message id
        mid = message_send(user['token'], channel_id, "user1")
        message_react(user['token'], mid, 1)
    response = channel_messages(user['token'], channel_id, 0)
    assert response['start'] == 0
    assert response['end'] == -1

    print("=========pass test4 : less than 50 messages======")


def test_channel_messages5():
    '''
    message is greater than 50
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    user1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    user2 = auth_register("123eff45", "xxx", "yyyy", email="he@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    channel_join(user1['token'], channel_id) #join user1 to channel
    channel_join(user2['token'], channel_id) #join user2 to channel
    i = 0
    while i < 50:
        i = i + 1
        message_send(user1['token'], channel_id, "user1")
    j = 0
    while j < 50:
        j = j + 1
        message_send(user2['token'], channel_id, "user2")

    response = channel_messages(user1['token'], channel_id, 0)
    assert response['start'] == 0
    assert response['end'] == 50

    print("=========pass test5 : messages from different user and number\
            of message is greater than 50========")


def test_channel_messages6():
    '''
    user not in the channel
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']

    user1 = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    with pytest.raises(ValueErr):
        channel_messages(user1['token'], channel_id, 1) #one is greater than 0
    print("========pass test6 : start point larger than number of messages")

def test_channel_messages7():
    '''
    react the message
    '''
    reset_data()
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    channel = channels_create(owner['token'], "hi", True)
    channel_id = channel['channel_id']
    msg_id = message_send(owner['token'], channel_id, "hi")
    message_react(owner['token'], msg_id, 1)

    result = channel_messages(owner['token'], channel_id, 0)
    message = result['messages']
    for i in message:
        for j in i['reacts']:
            assert(j['react_id']) == 1
