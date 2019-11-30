'''
include most of channel functions
'''
from error_handle import AccessError, ValueErr
import iter3 as func
import all_decos as deco

GETDATA = func.get_data
UPDATEDATA = func.update_data
GENERATEID = func.generate_id
GUFT = func.get_user_from_token
CHANNEL = func.Channel
FIND_MSG = func.find_msg
FIND_U = func.find_user
IS_CM = func.is_channel_member
IS_CO = func.is_channel_owner
GET_P = func.get_perm

SLACKR_OWNER = 1
SLACKR_ADMIN = 2
SLACKR_USER = 3
NAME_LEN = 20

@deco.get_u_token
def channels_create(user, name, is_public):
    """
    create a channel and return unique channel id
    """
    if not name or len(name) > NAME_LEN:
        raise ValueErr('invalid channel name')
    data = GETDATA()
    _list = [channel.channel_id for channel in data['channels']]
    channel_id = GENERATEID(_list)
    channel = CHANNEL(channel_id, name, is_public, [], [], [], [])

    u_id = user.u_id
    channel.add_owner(u_id)
    channel.add_member(u_id)
    data['channels'].append(channel)
    UPDATEDATA(data)

    return ({
        'channel_id': channel_id
    })

@deco.get_u_token
def channels_listall(user):
    '''
    list all the channle on the list
    '''
    data = GETDATA()

    new_list = []
    for channel in data['channels']:
        if not channel.is_public and not channel.is_member(user.u_id):
            continue
        new = {
            'channel_id': channel.channel_id,
            'name': channel.name,
        }
        new_list.append(new)

    return new_list

@deco.get_u_token
@deco.check_vchannel
@deco.check_vuid
def channel_invite(user, u_id, **kwargs):
    '''
    invite user to join in a channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()
    channel = data['channels'][index]
    # existence of the authorised user in a channel
    if not channel.is_member(user.u_id):
        raise AccessError('the authorised user is not a member of that channel')
    # existence of u_id user in a channel
    if channel.is_member(u_id):
        raise ValueErr('user is already in the channel')

    channel.add_member(u_id)
    # the invited user is slackr owner/admin
    if GET_P(u_id, data) != SLACKR_USER:
        channel.add_owner(u_id)
    UPDATEDATA(data)
    return {}

@deco.get_u_token
@deco.check_vchannel
def channel_details(user, **kwargs):
    '''
    let the members of channel get channel information
    '''
    data = GETDATA()
    index = kwargs['channel_index']
    channel = data['channels'][index]

    if not channel.is_public and not IS_CM(user.u_id, channel.channel_id, data):
        raise AccessError('Private channel!')

    owner_members = []
    for member in channel.owner_members:
        index = FIND_U(member, data)
        owner = data['users'][index]
        new_owner = {
            'u_id': member,
            'name_first': owner.name_first,
            'name_last': owner.name_last,
            'profile_img_url': owner.img_url
        }
        owner_members.append(new_owner)

    all_members = []
    for member in channel.all_members:
        index = FIND_U(member, data)
        tmp = data['users'][index]
        new_m = {
            'u_id': member,
            'name_first': tmp.name_first,
            'name_last': tmp.name_last,
            'profile_img_url': tmp.img_url
        }
        all_members.append(new_m)

    return ({
        'name': channel.name,
        'owner_members': owner_members,
        'all_members': all_members
    })

@deco.get_u_token
@deco.check_vchannel
def channel_leave(user, **kwargs):
    '''
    for user to leave a channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()
    channel = data['channels'][index]
    if channel.owner_members == [user.u_id]:
        raise AccessError('owner is the only owner in channel')

    if channel.is_owner(user.u_id):
        channel.remove_owner(user.u_id)
    channel.remove_member(user.u_id)

    UPDATEDATA(data)
    return {}

@deco.get_u_token
@deco.check_vchannel
def channel_join(user, **kwargs):
    '''
    let user join public channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()
    u_id = user.u_id
    channel = data['channels'][index]
    if not channel.is_public and GET_P(u_id, data) == SLACKR_USER:
        raise AccessError("Private channel!")

    channel.add_member(u_id)
    # the user is a slackr owner/admin
    if GET_P(u_id, data) != SLACKR_USER:
        channel.add_owner(u_id)
    UPDATEDATA(data)
    return {}

@deco.get_u_token
@deco.check_vchannel
def channel_addowner(owner, u_id, **kwargs):
    '''
    add owner of channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()
    channel = data['channels'][index]
    channel_id = channel.channel_id
    if channel.is_owner(u_id):
        raise ValueErr('user with user id u_id is already an owner of the channel')

    if not IS_CO(owner.u_id, channel_id, data):
        raise AccessError('the authorised user is not an admin of the channel')

    channel.add_owner(u_id)
    if not IS_CM(u_id, channel_id, data):
        channel.add_member(u_id)

    UPDATEDATA(data)
    return {}

@deco.get_u_token
@deco.check_vchannel
def channel_removeowner(user, u_id, **kwargs):
    '''
    remove owner of channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()
    channel = data['channels'][index]
    channel_id = channel.channel_id

    if not channel.is_owner(u_id):
        raise ValueErr('user with user id u_id is not an owner of the channel')

    if not IS_CO(user.u_id, channel_id, data):
        raise AccessError('the authorised user is not an admin of the channel')

    if user.permission_id == SLACKR_USER and GET_P(u_id, data) < SLACKR_USER:
        raise AccessError('User is not allowed to remove Slackr owner/admin')

    i = FIND_U(u_id, data)
    o_owner = data['users'][i]

    if channel.owner_members == [o_owner.u_id]:
        raise AccessError('cannot remove the only owner of channel')

    channel.remove_owner(o_owner.u_id)
    UPDATEDATA(data)
    return {}

@deco.get_u_token
def channels_list(user):
    '''
    list channels which the user joined in
    '''
    data = GETDATA()
    u_id = user.u_id
    new_list = []

    for channel in data['channels']:
        if channel.is_member(u_id):
            new = {
                'channel_id': channel.channel_id,
                'name': channel.name,
            }
            new_list.append(new)

    return new_list

@deco.get_u_token
@deco.check_vchannel
def channel_messages(user, start, **kwargs):
    '''
    show the messages post on channel
    '''
    index = kwargs['channel_index']
    data = GETDATA()

    channel = data['channels'][index]
    channel_id = channel.channel_id
    if len(channel.messages) < start:
        raise ValueErr('start is greater to the total number of messages in the channel')

    if not channel.is_public and not IS_CM(user.u_id, channel_id, data):
        raise AccessError('Private channel!')

    message_list = []
    end = start + 50

    channel = [x for x in data['channels'] if x.channel_id == channel_id][0]

    if end > len(channel.messages):
        end = -1
        for message_id_c in channel.messages[start:]:
            index = FIND_MSG(data['messages'], message_id_c)
            message = data['messages'][index]
            reacts = message.formatted_reacts(message.u_id)
            r_message = {
                'message_id': message.message_id,
                'u_id': message.u_id,
                'message': message.text,
                'time_created': message.time,
                'reacts': reacts,
                'is_pinned': message.is_pinned
            }

            message_list.append(r_message)

    else:
        for message_id_c in channel.messages[start:end]:
            index = FIND_MSG(data['messages'], message_id_c)
            message = data['messages'][index]
            reacts = message.formatted_reacts(message.u_id)
            r_message = {
                'message_id': message.message_id,
                'u_id': message.u_id,
                'message': message.text,
                'time_created': message.time,
                'reacts': reacts,
                'is_pinned': message.is_pinned
            }
            message_list.append(r_message)

    return {
        "messages" :message_list,
        "start": start,
        "end": end
    }
