"""
This file stores all standup related functions
"""
#pylint: disable=unused-argument
#pylint: disable-msg=too-many-function-args
#pylint: disable-msg=inconsistent-return-statements
import threading
from datetime import datetime, timedelta, timezone
from error_handle import AccessError, ValueErr
from iter3 import get_data, update_data, find_channel
from iter3 import is_channel_member, is_session_valid
from iter3 import generate_m_id, NewMessage
import all_decos as deco

MSG_LENGTH = 1000

@deco.get_u_token_k
@deco.check_vchannel
def standup_start(user, length, **kwargs):
    """
    Activate a standup session for the channel with channel_id
    """
    index = kwargs['channel_index']
    token = kwargs['token']
    data = get_data()

    channel = data['channels'][index]
    channel_id = channel.channel_id

    if not channel.is_member(user.u_id):
        raise AccessError('Permission denied')
    if channel.active_standup:
        raise ValueErr('An active standup is currently running in this channel')

    channel.active_standup = True
    time_future = datetime.utcnow()
    time_future += timedelta(seconds=length)
    timestamp = time_future.replace(tzinfo=timezone.utc).timestamp()
    channel.s_finish_time = timestamp
    update_data(data)

    timer = threading.Timer(length, standup_end, [token, channel_id])
    timer.start()
    return timestamp

@deco.get_u_token
def standup_end(user, channel_id, **kwargs):
    """
    Deactivate the standup, summarize and then send out messages
    """
    data = get_data()
    # make summary
    index = find_channel(data['channels'], channel_id)
    channel = data['channels'][index]
    buffer = channel.standup_buffer
    summary = ', '.join(buffer)
    # clear the buffer, remove standup details when the standup finishes
    channel.active_standup = False
    channel.s_finish_time = None
    channel.standup_buffer = []
    update_data(data)

    # send the summary
    data = get_data()
    # generating a new message object
    _list = [obj.message_id for obj in data['messages']]
    message_id = generate_m_id(_list)
    msg = NewMessage(user.u_id, channel_id, message_id, summary,
                     datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(),
                     {}, False)
    # add message in messages and channels
    index = find_channel(data['channels'], channel_id)
    channel = data['channels'][index]
    data['messages'].append(msg)
    channel.add_message(message_id)
    # update the database
    update_data(data)

@deco.get_u_token_k
@deco.check_vchannel
def standup_send(user, message, *args, **kwargs):
    """
    Send a message during the standup, message will be buffered
    """
    index = kwargs['channel_index']
    data = get_data()
    channel = data['channels'][index]
    channel_id = channel.channel_id

    if len(message) > MSG_LENGTH:
        raise ValueErr('Message is more than 1000 characters')
    if not message:
        return None

    #(channel.active_standup)
    if not channel.active_standup:
        raise ValueErr('An active standup is not currently running in this channel')

    if not is_channel_member(user.u_id, channel_id, data):
        raise AccessError('Permission denied')
    # added message to standup buffer
    send_m = user.handle + " : " + message
    channel.standup_buffer.append(send_m)
    update_data(data)
    # send out messages seperately
    # msg_id = message_send(kwargs['token'], channel_id, message)

@deco.check_vchannel
@deco.check_vtoken
def standup_active(**kwargs):
    """
    change standup active stage
    """
    data = get_data()
    index = kwargs['channel_index']
    channel = data['channels'][index]
    return channel.active_standup, channel.s_finish_time
