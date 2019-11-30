'''
This is a test file for message unreact
'''
#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args

import pytest
from error_handle import AccessError, ValueErr
from messages import message_send, message_remove
from messages import message_react, message_unreact
from channels import channels_create, channel_invite
from auths import auth_register
from iter3 import get_data, reset_data, find_msg

# ========== setup ==========
MESSAGE = 'This is a good MESSAGE'

@pytest.fixture
def setup_unreact():
    '''
    setup
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    token_s_o = owner['token']
    print(owner['u_id'])

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    token_c_o = c_owner['token']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hoi@gmail.com")
    token_c_m = c_mem['token']
    uid_cmem = c_mem['u_id']
    channel_invite(token_c_o, cid_0, uid_cmem)

    # pID = 3, a register user who created his own channel
    user = auth_register("123eff45", "xxx", "yyyy", email="hipp@gmail.com")
    token_user = user['token']
    channel_1 = channels_create(token_user, 'channel_1', True)
    cid_1 = channel_1['channel_id']

    return {
        'token_s_o': token_s_o,
        'token_c_o': token_c_o,
        'cid_0': cid_0,
        'token_c_m': token_c_m,
        'token_user': token_user,
        'cid_1': cid_1
    }
# ========== setup ==========

# ========== tests ==========

def test_member_unreact(setup_unreact):
    '''
    member unreact the message
    '''
    mid_c_o = message_send(setup_unreact['token_c_o'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_react(setup_unreact['token_c_m'], mid_c_o, 1)
    _ = message_unreact(setup_unreact['token_c_m'], mid_c_o, 1)
    data = get_data()
    i = find_msg(data['messages'], mid_c_o)
    assert not data['messages'][i].has_react_id(1)

def test_channel_owner_unreact(setup_unreact):
    '''
    channel owner unreact the message
    '''
    mid_cmem = message_send(setup_unreact['token_c_m'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_react(setup_unreact['token_c_o'], mid_cmem, 1)
    _ = message_unreact(setup_unreact['token_c_o'], mid_cmem, 1)
    data = get_data()
    i = find_msg(data['messages'], mid_cmem)
    assert not data['messages'][i].has_react_id(1)

def test_invalid_token(setup_unreact):
    '''
    invalid token
    '''
    mid_user = message_send(setup_unreact['token_user'],\
    setup_unreact['cid_1'], MESSAGE)
    _ = message_react(setup_unreact['token_user'], mid_user, 1)
    with pytest.raises(AccessError):
        message_unreact('tokenUnknown', mid_user, 1)

def test_invalid_unreact_id(setup_unreact):
    '''
    Invalid react_id
    '''
    mid_user = message_send(setup_unreact['token_user'],\
    setup_unreact['cid_1'], MESSAGE)
    _ = message_react(setup_unreact['token_user'], mid_user, 1)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_user'], mid_user, 100)

def test_never_ever_reacted(setup_unreact):
    '''
    Invalid react_id
    '''
    mid_user = message_send(setup_unreact['token_user'],\
    setup_unreact['cid_1'], MESSAGE)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_user'], mid_user, 1)

def test_message_doesnt_exist(setup_unreact):
    '''
    Message does not exist
    '''
    mid_c_o = message_send(setup_unreact['token_c_o'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_remove(setup_unreact['token_c_o'], mid_c_o)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_c_m'], mid_c_o, 1)

def test_not_in_joined_channel(setup_unreact):
    '''
    Invalid message_id
    '''
    mid_cmem = message_send(setup_unreact['token_c_m'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_react(setup_unreact['token_c_m'], mid_cmem, 1)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_user'], mid_cmem, 1)

def test_admin_owner_unreact(setup_unreact):
    '''
    Invalid message_id
    '''
    mid_user = message_send(setup_unreact['token_user'],\
    setup_unreact['cid_1'], MESSAGE)
    _ = message_react(setup_unreact['token_user'], mid_user, 1)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_s_o'], mid_user, 1)

def test_react_id_doesnt_exist(setup_unreact):
    '''
    React with react_id does not exist
    '''
    mid_cmem = message_send(setup_unreact['token_c_m'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_react(setup_unreact['token_c_o'], mid_cmem, 1)
    _ = message_unreact(setup_unreact['token_c_o'], mid_cmem, 1)
    with pytest.raises(ValueErr):
        message_unreact(setup_unreact['token_c_m'], mid_cmem, 1)

def test_unreact_others_react(setup_unreact):
    '''
    Cannot unreact others react
    '''
    mid_c_o = message_send(setup_unreact['token_c_o'],\
    setup_unreact['cid_0'], MESSAGE)
    _ = message_react(setup_unreact['token_c_m'], mid_c_o, 1)
    with pytest.raises(AccessError):
        _ = message_unreact(setup_unreact['token_c_o'], mid_c_o, 1)
