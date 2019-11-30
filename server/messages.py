'''
This file stores all message-related implementations
'''
#pylint: disable=unused-argument
import threading
from datetime import datetime, timezone
from error_handle import AccessError, ValueErr
from iter3 import NewMessage, generate_m_id
from iter3 import get_data, update_data
from iter3 import is_channel_owner, is_channel_member
from iter3 import find_channel, is_session_valid
import all_decos as deco

SLACKR_USER = 3
THUMBUP = 1
MSG_LENGTH = 1000

@deco.get_u_token
@deco.check_vchannel
def message_send(user, message, *args, **kwargs):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''
    index = kwargs['channel_index']
    data = get_data()
    channel_id = data['channels'][index].channel_id

    # message string restriction
    if len(message) > MSG_LENGTH:
        raise ValueErr('Message is too long')
    if not message:
        # raise ValueErr('Empty message is not allowed')
        return None
    # Existence of user in the channel
    if not data['channels'][index].is_member(user.u_id):
        raise AccessError('Not a member of the channel')

    # generating a new message object
    _list = [obj.message_id for obj in data['messages']]
    message_id = generate_m_id(_list)
    msg = NewMessage(user.u_id, channel_id, message_id, message,
                     datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(),
                     {}, False)

    # add message in messages and channels
    data['messages'].append(msg)
    data['channels'][index].add_message(message_id)
    # update the database
    update_data(data)
    return message_id

@deco.get_u_token
@deco.check_vmsg
def message_remove(user, message_id, *args, **kwargs):
    '''
    Given a message_id for a message, this message is removed from the channel
    '''
    index = kwargs['msg_index']
    data = get_data()
    # Accessibility
    sender_flag = False
    permission_flag = False
    # user is the sender
    if data['messages'][index].u_id == user.u_id:
        sender_flag = True
    # user is slackr owner or admin or channel owner
    if user.permission_id != SLACKR_USER:
        permission_flag = True
    else:
        if is_channel_owner(user.u_id, data['messages'][index].channel_id, data):
            permission_flag = True
    if not sender_flag and not permission_flag:
        raise AccessError("Permission denied")

    # delete message in channels and messages
    i = find_channel(data['channels'], data['messages'][index].channel_id)
    data['channels'][i].remove_message(message_id)
    del data['messages'][index]
    update_data(data)
    return {}

@deco.get_u_token
@deco.check_vmsg
def message_edit(user, message_id, message, *args, **kwargs):
    '''
    Given a message, update it's text with new text
    '''
    index = kwargs['msg_index']
    data = get_data()
    # message string restriction
    if len(message) > MSG_LENGTH:
        raise ValueErr('Message is too long')
    # Accessibility
    sender_flag = False
    permission_flag = False
    # user is the sender
    if data['messages'][index].u_id == user.u_id:
        sender_flag = True
    # user is slackr owner or admin or channel owner
    if user.permission_id != SLACKR_USER:
        permission_flag = True
    else:
        if is_channel_owner(user.u_id, data['messages'][index].channel_id, data):
            permission_flag = True
    if not sender_flag and not permission_flag:
        raise AccessError("Permission denied")

    # delete the original msg if length = 0
    if not message:
        c_id = data['messages'][index].channel_id
        c_index = find_channel(data['channels'], c_id)
        data['channels'][c_index].remove_message(message_id)
        del data['messages'][index]
        update_data(data)
        return {}
    # edit the message
    data['messages'][index].edit(message)
    update_data(data)
    return {}


@deco.get_u_token
@deco.check_vmsg
def message_react(user, message_id, react_id, *args, **kwargs):
    '''
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    '''
    index = kwargs['msg_index']
    data = get_data()
    # invalid react_id
    if react_id != THUMBUP:
        raise ValueErr("Invalid react_id")
    # Existence of message_id in a channel that the user has joined
    channel_id = data['messages'][index].channel_id
    i = find_channel(data['channels'], channel_id)
    if not data['channels'][i].is_member(user.u_id):
        raise ValueErr("Invalid message_id")

    # Existence of react
    if data['messages'][index].has_react_id(THUMBUP):
        raise ValueErr("React with react_id already exists")

    data['messages'][index].react(user.u_id, THUMBUP)
    update_data(data)
    return {}

@deco.get_u_token
@deco.check_vmsg
def message_unreact(user, message_id, react_id, *args, **kwargs):
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''
    index = kwargs['msg_index']
    data = get_data()
    # invalid react_id
    if react_id != THUMBUP:
        raise ValueErr("Invalid react_id")
    # Existence of message_id in a channel that the user has joined
    channel_id = data['messages'][index].channel_id
    i = find_channel(data['channels'], channel_id)
    if not data['channels'][i].is_member(user.u_id):
        raise ValueErr("Invalid message_id")

    # Existence of react_id
    if not data['messages'][index].has_react_id(THUMBUP):
        raise ValueErr("React with react_id does not exist")
    if user.u_id in data['messages'][index].reacts[THUMBUP]:
        data['messages'][index].unreact(user.u_id, THUMBUP)
    else:
        raise AccessError("Cannot unreact others react")
    update_data(data)
    return {}

@deco.get_u_token
@deco.check_vmsg
@deco.check_pinned
def message_pin(user, message_id, *args, **kwargs):
    '''
    Given a message within a channel, mark it as "pinned" to be
    given special display treatment by the frontend
    '''
    index = kwargs['msg_index']
    data = get_data()
    # user is not a member of the channel
    channel_id = data['messages'][index].channel_id
    if not is_channel_member(user.u_id, channel_id, data):
        raise AccessError("User is not a member of the channel")
    # Admin of the channel
    if (user.permission_id == SLACKR_USER and not \
    is_channel_owner(user.u_id, channel_id, data)):
        raise ValueErr("User is not an admin of the channel")

    # pin the message
    data['messages'][index].pin()
    c_index = find_channel(data['channels'], channel_id)
    data['channels'][c_index].pin_message(message_id)
    update_data(data)
    return {}


@deco.get_u_token
@deco.check_vmsg
@deco.check_unpinned
def message_unpin(user, message_id, *args, **kwargs):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''
    index = kwargs['msg_index']
    data = get_data()

    # user is not a member of the channel
    channel_id = data['messages'][index].channel_id
    if not is_channel_member(user.u_id, channel_id, data):
        raise AccessError("User is not a member of the channel")
    # Admin of the channel
    if (user.permission_id == SLACKR_USER and not\
     is_channel_owner(user.u_id, channel_id, data)):
        raise ValueErr("User is not an admin of the channel")

    # unpin the message
    data['messages'][index].unpin()
    c_index = find_channel(data['channels'], channel_id)
    data['channels'][c_index].unpin_message(message_id)
    update_data(data)
    return {}

@deco.check_vtoken
def search_message(query_string):
    '''
    Given a query string, return a collection of messages in
    all of the channels that the user has joined that match the query
    '''
    data = get_data()
    _list = []
    # list all the channels a user join
    query_string = str(query_string)
    for msg in data['messages']:
        if query_string in msg.text:
            new = {
                'message_id': msg.message_id,
                'u_id': msg.u_id,
                'message': msg.text,
                'time_created': msg.time,
                'reacts': msg.formatted_reacts(msg.u_id),
                'is_pinned': msg.is_pinned
            }
            _list.append(new)
    return _list

@deco.get_u_token_k
@deco.check_vchannel
def message_sendlater(user, message, time_sent, **kwargs):
    '''
    Error checking function for sendlater
    '''
    data = get_data()
    index = kwargs['channel_index']
    channel_id = data['channels'][index].channel_id
    token = kwargs['token']

    # message string restriction
    if len(message) > MSG_LENGTH:
        raise ValueErr('Message is too long')
    if not message:
        return None
    # Existence of user in the channel
    if not data['channels'][index].is_member(user.u_id):
        raise AccessError('Not a member of the channel')
    # future time
    timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    if time_sent < timestamp:
        raise ValueErr("Time sent is a time in the past")

    _list = [obj.message_id for obj in data['messages']]
    message_id = generate_m_id(_list)
    data['messages_buffer'] += 1
    update_data(data)

    # start the timer
    timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    length = time_sent - timestamp
    timer = threading.Timer(length, send_now,
                            [token, channel_id, message, message_id])
    timer.start()
    return message_id

@deco.get_u_token
def send_now(user, channel_id, message, message_id):
    '''
    triggering the message to be sent when reaches the specified time
    '''
    data = get_data()
    index = find_channel(data['channels'], channel_id)
    msg = NewMessage(user.u_id, channel_id, message_id, message,\
    datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(), {}, False)
    data['messages'].append(msg)
    data['channels'][index].add_message(message_id)
    update_data(data)
