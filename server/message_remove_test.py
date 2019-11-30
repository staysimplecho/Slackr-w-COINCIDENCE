'''
This is a test file for message remove
'''
#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args
import pytest
from error_handle import AccessError, ValueErr
from messages import message_send, message_remove
from channels import channels_create, channel_invite
from auths import auth_register
from iter3 import get_data, reset_data, find_msg

# ========== setup ==========
MESSAGE = 'This is a good MESSAGE'

@pytest.fixture
def setup_remove():
    '''
    setup
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    token_s_o = owner['token']
    uid_so = owner['u_id']

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    token_c_o = c_owner['token']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hwo@gmail.com")
    token_c_m = c_mem['token']
    uid_cmem = c_mem['u_id']
    channel_invite(token_c_o, cid_0, uid_cmem)

    # pID = 3, a register user who created his own channel
    user = auth_register("123eff45", "xxx", "yyyy", email="hp@gmail.com")
    token_user = user['token']
    channel_1 = channels_create(token_user, 'channel_1', True)
    cid_1 = channel_1['channel_id']
    channel_invite(token_user, cid_1, uid_so)

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

def test_sender_del_his_own(setup_remove):
    '''
    a sender delete his own message
    '''
    mid_cmem = message_send(setup_remove['token_c_m'],\
    setup_remove['cid_0'], MESSAGE)
    _ = message_remove(setup_remove['token_c_m'], mid_cmem)
    data = get_data()
    i = find_msg(data['messages'], mid_cmem)
    assert i is None

def test_admin_owner_del_anyone(setup_remove):
    '''
    admin or owner delete other user's message
    '''
    mid_user = message_send(setup_remove['token_user'],\
    setup_remove['cid_1'], MESSAGE)
    _ = message_remove(setup_remove['token_s_o'], mid_user)
    data = get_data()
    i = find_msg(data['messages'], mid_user)
    assert i is None

def test_channel_owner_del_his_own(setup_remove):
    '''
    channel owner delete his own message
    '''
    mid_cowner = message_send(setup_remove['token_c_o'],
                              setup_remove['cid_0'], MESSAGE)
    _ = message_remove(setup_remove['token_c_o'], mid_cowner)
    data = get_data()
    i = find_msg(data['messages'], mid_cowner)
    assert i is None

def test_channel_owner_del_member(setup_remove):
    '''
    channel owner delete member's message
    '''
    mid_cmem = message_send(setup_remove['token_c_m'],\
    setup_remove['cid_0'], MESSAGE)
    _ = message_remove(setup_remove['token_c_o'], mid_cmem)
    data = get_data()
    i = find_msg(data['messages'], mid_cmem)
    assert i is None

def test_invalid_token(setup_remove):
    '''
    token is invalid
    '''
    mid_0 = message_send(setup_remove['token_user'],
                         setup_remove['cid_1'], MESSAGE)
    with pytest.raises(AccessError):
        message_remove('tokenUnknown', mid_0)

def test_message_doesnt_exist(setup_remove):
    '''
    Message no longer exists
    '''
    mid_sou = message_send(setup_remove['token_s_o'],
                           setup_remove['cid_1'], MESSAGE)
    _ = message_remove(setup_remove['token_s_o'], mid_sou)
    with pytest.raises(ValueErr):
        message_remove(setup_remove['token_s_o'], mid_sou)

def test_restricted(setup_remove):
    '''
    Permission denied
    '''
    mid_cmem = message_send(setup_remove['token_c_m'],
                            setup_remove['cid_0'], MESSAGE)
    with pytest.raises(AccessError):
        message_remove(setup_remove['token_user'], mid_cmem)
