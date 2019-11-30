#pylint: disable-msg=too-many-function-args
"""
This is a test file which contains two different cases built to test search function.
"""
from datetime import datetime, timezone
from iter3 import reset_data
from messages import message_send, message_react, search_message
from auths import auth_register
from channels import channels_create, channel_invite

STRING = 'a' * 2000

def test_search_message1():
    """
    test if function works out with message_send, message_react
    by comparing result with expected answer
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw1@gmail.com")
    token1 = user1['token']
    channel01 = channels_create(token1, 'channel01', True)
    user2 = auth_register("1234567", "un", "sw", email="unsw2@gmail.com")
    token2 = user2['token']
    channel_invite(token1, channel01['channel_id'], user2['u_id'])
    msg1 = message_send(token1, channel01['channel_id'], 'hi321')
    message_react(token1, msg1, 1)
    msg2 = message_send(token1, channel01['channel_id'], 'hi1')
    message_react(token2, msg2, 1)
    msg = search_message(token1, 'hi')
    curr_time = datetime.utcnow()
    timestamp = curr_time.replace(tzinfo=timezone.utc).timestamp()
    expected = [
        {
            'is_pinned': False,
            'message': 'hi321',
            'message_id': 1,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [0],
                    'is_this_user_reacted': True
                }
            ],
            'time_created': timestamp,
            'u_id': 0
        },
        {
            'is_pinned': False,
            'message': 'hi1',
            'message_id': 2,
            'reacts': [{
                'react_id': 1,
                'u_ids': [1],
                'is_this_user_reacted': False
            }],
            'time_created': timestamp,
            'u_id': 0
        }
    ]
    assert msg[0]['is_pinned'] == expected[0]['is_pinned']
    assert msg[0]['message'] == expected[0]['message']
    assert msg[0]['message_id'] == expected[0]['message_id']
    assert msg[0]['reacts'] == expected[0]['reacts']
    assert msg[0]['u_id'] == expected[0]['u_id']
    assert msg[0]['time_created'] - expected[0]['time_created'] < 1

    assert msg[1]['is_pinned'] == expected[1]['is_pinned']
    assert msg[1]['message'] == expected[1]['message']
    assert msg[1]['message_id'] == expected[1]['message_id']
    assert msg[1]['reacts'] == expected[1]['reacts']
    assert msg[1]['u_id'] == expected[1]['u_id']
    assert msg[1]['time_created'] - expected[1]['time_created'] < 1
    print("=============pass test1 : 'hi321 and hi1 are in the lists' ============")


def test_search_message2():
    """
    test if function works out if no msg found
    """
    reset_data()
    user1 = auth_register("1234567", "un", "sw", email="unsw@gmail.com")
    token = user1['token']
    channel01 = channels_create(token, 'channel01', True)
    _ = message_send(token, channel01['channel_id'], 'yu321')
    msg = search_message(token, 'hi')
    assert not msg
    print("=============pass test2 : nothing in the lists' ============")
