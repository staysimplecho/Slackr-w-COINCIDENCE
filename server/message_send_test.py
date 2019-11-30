'''
This is a test file for message send
'''
#pylint: disable=redefined-outer-name
#pylint: disable=too-many-function-args
import pytest
from error_handle import AccessError, ValueErr
from messages import message_send
from channels import channels_create, channel_invite
from auths import auth_register
from iter3 import get_data, reset_data, find_msg


# ========== setup ==========
MESSAGE = 'This is a good MESSAGE'

@pytest.fixture
def setup_send():
    '''
    set up
    '''
    reset_data()
    print("===================data reseted===================")
    # pId = 1, owner of the Slackr
    owner = auth_register("123eff45", "xxx", "yyyy", email="hwi@gmail.com")
    token_s_o = owner['token']

    # pID = 3, a channel owner
    c_owner = auth_register("123eff45", "xxx", "yyyy", email="hw@gmail.com")
    token_c_o = c_owner['token']
    channel_0 = channels_create(token_c_o, 'channel_0', True)
    cid_0 = channel_0['channel_id']

    # pID = 3, a channel_member
    c_mem = auth_register("123eff45", "xxx", "yyyy", email="hpi@gmail.com")
    token_c_m = c_mem['token']
    uid_cmem = c_mem['u_id']
    channel_invite(token_c_o, cid_0, uid_cmem)

    # pID = 3, a register user who hasn't joined in any channels
    user = auth_register("123eff45", "xxx", "yyyy", email="hwio@gmail.com")
    token_user = user['token']

    return {
        'token_s_o': token_s_o,
        'token_c_o': token_c_o,
        'cid_0': cid_0,
        'token_c_m': token_c_m,
        'token_user': token_user
    }

# ========== setup ==========

# ========== tests ==========

def test_send_ok(setup_send):
    '''
    check if the msg is sent
    '''
    message_id = message_send(setup_send['token_c_m'], setup_send['cid_0'], MESSAGE)
    data = get_data()
    assert find_msg(data['messages'], message_id) == 0

def test_invalid_token(setup_send):
    '''
    Invalid token
    '''
    with pytest.raises(AccessError):
        message_send('tokenUnknown', setup_send['cid_0'], MESSAGE)

def test_length_over(setup_send):
    '''
    message is too long
    '''
    with pytest.raises(ValueErr):
        message_send(setup_send['token_c_m'], setup_send['cid_0'], 'a'*1001)

def test_invalid_channel_id(setup_send):
    '''
    invalid channel_id
    '''
    with pytest.raises(ValueErr):
        message_send(setup_send['token_c_o'], -1, MESSAGE)

def test_not_a_member(setup_send):
    '''
    not a member of the channel
    '''
    with pytest.raises(AccessError):
        message_send(setup_send['token_user'], setup_send['cid_0'], MESSAGE)

def test_slackr_owner_send(setup_send):
    '''
    owner not in the channel
    '''
    with pytest.raises(AccessError):
        message_send(setup_send['token_s_o'], setup_send['cid_0'], MESSAGE)
