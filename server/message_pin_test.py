'''
This is a test file for message pin
'''
#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args


import pytest
from error_handle import AccessError, ValueErr
from messages import message_send, message_pin, message_remove
from channels import channels_create, channel_invite
from auths import auth_register, admin_userpermission_change
from iter3 import get_data, reset_data, find_channel

# ========== setup ==========
MESSAGE = 'This is a good MESSAGE'

@pytest.fixture
def setup_pin():
    '''
    setup
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    token_s_o = owner['token']

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hiw@gmail.com")
    token_c_o = c_owner['token']
    uid_c_o = c_owner['u_id']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']
    # promote this channel owner to slackr admin
    admin_userpermission_change(token_s_o, 2, uid_c_o)

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hwo@gmail.com")
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
        'cid_0': cid_0,
        'token_c_o': token_c_o,
        'token_c_m': token_c_m,
        'cid_1': cid_1,
        'token_user': token_user
    }
# ========== setup ==========

# ========== tests ==========
def test_admin_pin(setup_pin):
    '''
    test admin to pin message
    '''
    mid_cmem0 = message_send(setup_pin['token_c_m'],\
    setup_pin['cid_0'], MESSAGE)
    _ = message_pin(setup_pin['token_c_o'], mid_cmem0)
    data = get_data()
    i = find_channel(data['channels'], setup_pin['cid_0'])
    assert mid_cmem0 in data['channels'][i].pinned

def test_invalid_token(setup_pin):
    '''
    Invalid token
    '''
    mid_user0 = message_send(setup_pin['token_user'],\
    setup_pin['cid_1'], MESSAGE)
    with pytest.raises(AccessError):
        message_pin('tokenUnknown', mid_user0)

def test_message_doesnt_exist(setup_pin):
    '''
    Invalid message_id
    '''
    mid_user0 = message_send(setup_pin['token_user'],\
    setup_pin['cid_1'], MESSAGE)
    _ = message_remove(setup_pin['token_user'], mid_user0)
    with pytest.raises(ValueErr):
        message_pin(setup_pin['token_user'], mid_user0)

def test_already_pinned(setup_pin):
    '''
    Message is already pinned
    '''
    mid_cmem0 = message_send(setup_pin['token_c_m'],\
    setup_pin['cid_0'], MESSAGE)
    _ = message_pin(setup_pin['token_c_o'], mid_cmem0)
    with pytest.raises(ValueErr):
        message_pin(setup_pin['token_c_o'], mid_cmem0)

def test_slackr_owner_not_a_member(setup_pin):
    '''
    User is not a member of the channel
    '''
    mid_co = message_send(setup_pin['token_c_o'],\
    setup_pin['cid_0'], MESSAGE)
    with pytest.raises(AccessError):
        message_pin(setup_pin['token_s_o'], mid_co)

def test_member_not_an_admin(setup_pin):
    '''
    User is not an admin
    '''
    mid_cmem0 = message_send(setup_pin['token_c_o'],\
    setup_pin['cid_0'], MESSAGE)
    with pytest.raises(ValueErr):
        message_pin(setup_pin['token_c_m'], mid_cmem0)
