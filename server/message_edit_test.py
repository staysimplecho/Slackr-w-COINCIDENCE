'''
This file is to test message_edit
'''

#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args
import pytest
from error_handle import AccessError, ValueErr
from messages import message_send, message_edit
from channels import channels_create, channel_invite
from auths import auth_register
from iter3 import get_data, reset_data, find_msg

#global variables below
MESSAGE = 'This is a good MESSAGE'
#global variables above

@pytest.fixture
def setup_edit():
    '''
    this is a setup function
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hi@gmail.com")
    token_s_o = owner['token']

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hii@gmail.com")
    token_c_o = c_owner['token']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    token_c_m = c_mem['token']
    uid_cmem = c_mem['u_id']
    channel_invite(token_c_o, cid_0, uid_cmem)

    # pID = 3, a register user who hasn't joined in any channels
    user = auth_register("123eff45", "xxx", "yyyy", email="hoi@gmail.com")
    token_user = user['token']

    mid_cowner = message_send(token_c_o, cid_0, MESSAGE)
    mid_cmem = message_send(token_c_m, cid_0, MESSAGE)

    return {
        'token_s_o': token_s_o,
        'token_c_o': token_c_o,
        'cid_0': cid_0,
        'token_c_m': token_c_m,
        'token_user': token_user,
        'mid_cowner': mid_cowner,
        'mid_cmem': mid_cmem
    }


# ========== setup ==========

# ========== tests ==========

def test_sender_edit_his_own(setup_edit):
    '''
    edit the messages
    '''
    _ = message_edit(setup_edit['token_c_m'], setup_edit['mid_cmem'], 'cmemb edited his own')
    data = get_data()
    i = find_msg(data['messages'], setup_edit['mid_cmem'])
    assert data['messages'][i].text == 'cmemb edited his own'

def test_admin_owner_edit_not_his_own(setup_edit):
    '''
    owner edit the messages
    '''
    _ = message_edit(setup_edit['token_s_o'], setup_edit['mid_cowner'], 'slackr owner edited')
    data = get_data()
    i = find_msg(data['messages'], setup_edit['mid_cowner'])
    assert data['messages'][i].text == 'slackr owner edited'

def test_channel_owner_edit_his_own(setup_edit):
    '''
    channel owner edit his messages
    '''
    _ = message_edit(setup_edit['token_c_o'], setup_edit['mid_cowner'], \
    'channel owner edited his own')
    data = get_data()
    i = find_msg(data['messages'], setup_edit['mid_cowner'])
    assert data['messages'][i].text == 'channel owner edited his own'

def test_channel_owner_edit_not_his_own(setup_edit):
    '''
    channel owner edited
    '''
    _ = message_edit(setup_edit['token_c_o'], setup_edit['mid_cmem'], 'channel owner edited')
    data = get_data()
    i = find_msg(data['messages'], setup_edit['mid_cmem'])
    assert data['messages'][i].text == 'channel owner edited'

def test_length_zero(setup_edit):
    '''
    edit nothing
    '''
    _ = message_edit(setup_edit['token_c_m'], setup_edit['mid_cmem'], '')
    data = get_data()
    assert find_msg(data['messages'], setup_edit['mid_cmem']) is None

def test_invalid_token(setup_edit):
    '''
    invalid token
    '''
    with pytest.raises(AccessError):
        message_edit('tokenUnknown', setup_edit['cid_0'], "edit")

def test_message_doesnt_exist(setup_edit):
    '''
    message no longer exists
    '''
    with pytest.raises(ValueErr):
        message_edit(setup_edit['token_s_o'], -1, 'whatever')

def test_length_over(setup_edit):
    '''
    Message is too long
    '''
    with pytest.raises(ValueErr):
        message_edit(setup_edit['token_s_o'], setup_edit['mid_cmem'], 'a'*1001)

def test_restricted(setup_edit):
    '''
    Permission denied
    '''
    with pytest.raises(AccessError):
        message_edit(setup_edit['token_user'], setup_edit['mid_cowner'], 'hack in')
