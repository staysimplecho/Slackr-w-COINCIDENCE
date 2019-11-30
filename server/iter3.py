#pylint: disable-msg=too-many-arguments
#pylint: disable-msg=too-many-instance-attributes
'''
This module stores the data structures we created and a bunch of
helper functions that will be used throughout the development.
'''
import os
import hashlib
import pickle
from datetime import datetime, timezone
import random
import string
import jwt

from error_handle import ValueErr

SECRET = 'comp153331'
CODE_LENGTH = 6

'''
Construction of Data Structures
'''
DB = {
    'owner': None,
    'admins': [], # list of user objects
    'users':[], # list of user objects
    'channels': [], # list of channel objects
    'messages': [],  # list of message objects
    'login_users': [], # list of logged-in user tokens
    'reset_users': [], # list of dics, dic = {uid, reset_code}
    'messages_buffer': 0
}

class User:
    '''
    User class that store any info related to a user
    '''
    def __init__(self, u_id, email, password, name_first,
                 name_last, handle, permission_id, host):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle
        # Slackr owner = 1, Slackr admin = 2, others = 3
        self.permission_id = permission_id
        self.img_url = host

    def add_avatar(self, url):
        ''' method for adding the user's profile image url '''
        self.img_url = url

    def reset_password(self, new):
        ''' method for resetting the user's password '''
        self.password = hash_password(new)

    def reset_handle(self, new):
        ''' method for resetting the user's handle '''
        self.handle = new

    def reset_email(self, new):
        ''' method for resetting the user's email '''
        self.email = new

    def reset_names(self, first_name, last_name):
        ''' method for resetting the user's names '''
        self.name_first = first_name
        self.name_last = last_name


class NewMessage:
    '''
    Message class for constructing a message that has info stored in it
    '''
    def __init__(self, u_id, channel_id, message_id,
                 text, time, reacts, is_pinned):
        self.u_id = u_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.text = text
        self.time = time
        self.reacts = reacts # {} to initialize
        '''
        reacts = {
            'react_id_1': [u_id_1, u_id_2, ...],
            'react_id_2': [u_id_3, ...],
            ......
        }
        '''
        self.is_pinned = is_pinned  # False to initialize

    def edit(self, msg):
        ''' method for replacing message.text with msg '''
        self.text = msg

    def pin(self):
        ''' method for marking the message as pinned '''
        self.is_pinned = True

    def unpin(self):
        ''' method for marking the message as unpinned '''
        self.is_pinned = False

    def has_react_id(self, react_id):
        '''
        method for checking if the message has been
        reacted with react_id
        '''
        return react_id in self.reacts

    def react(self, u_id, react_id):
        '''
        method for adding a react with react_id to the message
        '''
        if self.has_react_id(react_id):
            self.reacts[react_id].append(u_id)
        else:
            self.reacts[react_id] = []
            self.reacts[react_id].append(u_id)

    def unreact(self, u_id, react_id):
        '''
        method for removing a react with react_id from the message
        '''
        if u_id in self.reacts[react_id]:
            self.reacts[react_id].remove(u_id)
            if not self.reacts[react_id]:
                del self.reacts[react_id]

    def formatted_reacts(self, u_id):
        '''
        method for returning a list of reacts using expected format
        '''
        formatted = []
        if not self.reacts:
            return []
        for rids, uids in self.reacts.items():
            is_this_user_reacted = False
            if u_id in uids:
                is_this_user_reacted = True
            formatted.append({
                'react_id': rids,
                'u_ids': uids,
                'is_this_user_reacted': is_this_user_reacted
            })
        return formatted

class Channel:
    '''
    Channel class that store any info related to a channel
    '''
    def __init__(self, channel_id, name, is_public, owner_member,
                 all_member, messages, pinned):
        self.channel_id = channel_id
        self.name = name
        self.is_public = is_public
        self.owner_members = owner_member # [] to initialize, list of u_id
        self.all_members = all_member # [] to initialize, list of u_id
        self.messages = messages # [] to initialize, list of message_id
        self.pinned = pinned # [] to initialize, list of message_id
        self.active_standup = False
        self.standup_buffer = []
        self.s_finish_time = None

    def add_owner(self, owner_id):
        ''' method for adding a user to the owner list '''
        self.owner_members.append(owner_id)

    def add_member(self, member_id):
        ''' method for adding a user to the member list '''
        self.all_members.append(member_id)

    def remove_owner(self, owner_id):
        ''' method for removing a user to the owner list '''
        self.owner_members.remove(owner_id)

    def remove_member(self, member_id):
        ''' method for removing a user to the member list '''
        self.all_members.remove(member_id)

    def add_message(self, message_id):
        ''' method for adding a new message to the channel '''
        self.messages.append(message_id)

    def remove_message(self, message_id):
        ''' method for removing an existing message from the channel '''
        self.messages.remove(message_id)

    def pin_message(self, message_id):
        '''
        method for adding an existing message within the channel
        to the pinned message list
        '''
        self.pinned.append(message_id)

    def unpin_message(self, message_id):
        '''
        method for removing an existing message within the channel
        from the pinned message list
        '''
        self.pinned.remove(message_id)

    def is_member(self, u_id):
        '''
        method for checking id a user with u_id is a member of the channel
        '''
        return u_id in self.all_members

    def is_owner(self, u_id):
        '''
        method for checking id a user with u_id is an owner of the channel
        '''
        return u_id in self.owner_members

# helper function for generating uniq ID
def generate_id(id_list):
    '''
    helper function for generating uniq ID
    '''
    if not id_list:
        return 0
    return id_list[-1] + 1

def generate_m_id(id_list):
    """
    special generate algorithm for msg id
    as buffer messages generated by send-later funtion
    """
    data = get_data()
    if not id_list:
        return data['messages_buffer'] + 1
    return id_list[-1] + data['messages_buffer'] + 1

# helper functions for getting/setting global variables and database file
def get_data():
    '''
    get data from DATA.p
    '''
    try:
        file_length = os.stat("DATA.p").st_size
    except FileNotFoundError:
        file_length = 0

    if file_length == 0:
        database = {
            'users':[],
            'channels': [],
            'messages': [],
            'login_users': [],
            'reset_users': [],
            'messages_buffer': 0
        }
        return database

    with open('DATA.p', 'rb') as file:
        database = pickle.load(file)
    return database

def update_data(database):
    '''
    update DATA.p
    '''
    with open('DATA.p', 'wb') as file:
        pickle.dump(database, file)

def reset_data():
    '''
    clear data and initialize DATA.p
    '''
    database = {
        'users':[],
        'channels': [],
        'messages': [],
        'login_users': [],
        'reset_users': [],
        'messages_buffer': 0
    }
    with open('DATA.p', 'wb') as file:
        pickle.dump(database, file)


# helper functions related to token generation and info extraction
def hash_password(password):
    ''' generate SHA256 encrypted password '''
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(email, u_id, name_first, name_last):
    ''' generate token using JWT '''
    payload = {
        'email': email,
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    }
    encoded = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
    return encoded # return token in utf-8 string format

def get_user_from_token(token):
    '''
    decrypt token and return user info that was stored in payload
    '''
    try:
        payload = jwt.decode(bytes(token, 'utf-8'), SECRET,
                             algorithms='HS256')
    except Exception:
        raise ValueErr("error_handle occurs when decoding token")
    return payload # dictionary

# helper functions for checking permission
def is_session_valid(token, data):
    ''' check if the token is a valid token that belongs to a logged-in user '''
    return token in data['login_users']

def is_channel_owner(u_id, channel_id, data):
    ''' check if the user with token is an owner of channel with channel_id '''
    index = find_channel(data['channels'], channel_id)
    if index is None:
        return False
    if data['channels'][index].is_owner(u_id):
        return True
    return False

def is_channel_member(u_id, channel_id, data):
    ''' check if the user with token is a memeber of channel with channel_id '''
    index = find_channel(data['channels'], channel_id)
    if index is None:
        return False
    if data['channels'][index].is_member(u_id):
        return True
    return False

def is_user(u_id, data):
    ''' check if the user with token is a registered user of the Slackr '''
    return any(u_id == user.u_id for user in data['users'])

def get_perm(u_id, data):
    ''' return the permission_id of user with u_id '''
    index = find_user(u_id, data)
    if index is None:
        raise ValueErr('User does not exist')
    return data['users'][index].permission_id


# Finder functions
def find_user(u_id, data):
    ''' find the index of a user with u_id in a date['users'] list'''
    i = 0
    while i < len(data['users']):
        if data['users'][i].u_id == u_id:
            return i
        i += 1
    return None

def find_msg(messages, message_id):
    ''' find the index of a message with message_id in data['messages'] list '''
    i = 0
    while i < len(messages):
        if messages[i].message_id == message_id:
            return i
        i += 1
    return None

def find_channel(channels, channel_id):
    ''' find the index of a channle with channel_id in data['channels'] list '''
    i = 0
    while i < len(channels):
        if channels[i].channel_id == channel_id:
            return i
        i += 1
    return None

def handle_exists(handle, data):
    ''' check if the given handle already belongs to an existing user '''
    handles = [user.handle for user in data['users']]
    return handle in handles

# helper function for generating uniq string
def generate_random_string():
    '''
    generate a random string as password reset verification code
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(CODE_LENGTH))
