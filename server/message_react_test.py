'''
This is a test file for message react
'''
#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args

import pytest
from error_handle import AccessError, ValueErr
from messages import message_send, message_react, message_remove
from channels import channels_create, channel_invite
from auths import auth_register
from iter3 import get_data, reset_data, find_msg

# ========== setup ==========
MESSAGE = 'This is a good MESSAGE'

@pytest.fixture
def setup_react():
    '''
    setup
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    token_s_o = owner['token']

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hwu@gmail.com")
    token_c_o = c_owner['token']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    token_c_m = c_mem['token']
    uid_cmem = c_mem['u_id']
    channel_invite(token_c_o, cid_0, uid_cmem)

    # pID = 3, a register user who created his own channel
    user = auth_register("123eff45", "xxx", "yyyy", email="hwp@gmail.com")
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

def test_member_react(setup_react):
    '''
    test if a memer can react message
    '''
    mid_cmem = message_send(setup_react['token_c_m'],\
    setup_react['cid_0'], MESSAGE)
    _ = message_react(setup_react['token_c_m'], mid_cmem, 1)
    data = get_data()
    i = find_msg(data['messages'], mid_cmem)
    assert data['messages'][i].has_react_id(1)

def test_channel_owner_react_member(setup_react):
    '''
    test if channel owner can react member's message
    '''
    mid_cmem = message_send(setup_react['token_c_m'],\
    setup_react['cid_0'], MESSAGE)
    _ = message_react(setup_react['token_c_o'], mid_cmem, 1)
    data = get_data()
    i = find_msg(data['messages'], mid_cmem)
    assert data['messages'][i].has_react_id(1)

def test_invalid_token(setup_react):
    '''
    token is not valid
    '''
    mid_user = message_send(setup_react['token_user'],\
    setup_react['cid_1'], MESSAGE)
    with pytest.raises(AccessError):
        message_react('tokenUnknown', mid_user, 1)

def test_invalid_react_id(setup_react):
    '''
    react id is not valid
    '''
    mid_user = message_send(setup_react['token_user'],\
    setup_react['cid_1'], MESSAGE)
    with pytest.raises(ValueErr):
        message_react(setup_react['token_user'], mid_user, 0)

def test_message_doesnt_exist(setup_react):
    '''
    message does not exist
    '''
    mid_user = message_send(setup_react['token_user'],\
    setup_react['cid_1'], MESSAGE)
    _ = message_remove(setup_react['token_user'], mid_user)
    with pytest.raises(ValueErr):
        message_react(setup_react['token_user'], mid_user, 1)

def test_not_in_joined_channel(setup_react):
    '''
    message id is invalid
    '''
    mid_cmem = message_send(setup_react['token_c_m'],\
    setup_react['cid_0'], MESSAGE)
    with pytest.raises(ValueErr):
        message_react(setup_react['token_user'], mid_cmem, 1)

def test_admin_owner_react_anyone(setup_react):
    '''
    message id is invalid
    '''
    mid_user0 = message_send(setup_react['token_user'],\
    setup_react['cid_1'], MESSAGE)
    with pytest.raises(ValueErr):
        message_react(setup_react['token_s_o'], mid_user0, 1)

def test_react_id_already_exist(setup_react):
    '''
    React with react_id already exist
    '''
    mid_cmem = message_send(setup_react['token_c_m'],\
    setup_react['cid_0'], MESSAGE)
    _ = message_react(setup_react['token_c_m'], mid_cmem, 1)
    with pytest.raises(ValueErr):
        message_react(setup_react['token_c_o'], mid_cmem, 1)
