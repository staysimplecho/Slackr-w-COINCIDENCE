""" This file stores decorator functions """
import re
from error_handle import ValueErr, AccessError
from iter3 import get_data, is_session_valid, find_msg
from iter3 import find_channel, is_user, find_user, get_user_from_token

PATTERN = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
NAME_LEN = 50
PW_LENGTH = 6
HANDLE_LOWER = 3
HANDLE_UPPER = 20

def check_vtoken(function):
    """ decorator function for checking if the token is valid """
    def wrapper(*args, **kwargs):
        data = get_data()
        if not is_session_valid(args[0], data):
            raise AccessError('Invalid token')
        args = args[1:]
        return function(*args, **kwargs)
    return wrapper

def check_vchannel(function):
    """ decorator function for checking if a channel exists """
    def wrapper(user, channel_id, *args, **kwargs):
        data = get_data()
        index = find_channel(data['channels'], channel_id)
        if index is None:
            raise ValueErr("Invalid channel_id")
        kwargs['channel_index'] = index
        return function(user, *args, **kwargs)
    return wrapper

def check_vpassword(function):
    """ decorator function for checking if the token is valid """
    def wrapper(*args, **kwargs):
        if not args[0] or len(args[0]) < PW_LENGTH:
            raise ValueErr('Invalid password')
        return function(*args, **kwargs)
    return wrapper

def check_vmsg(function):
    """ decorator function for checking if the message exists """
    def wrapper(token, message_id, *args, **kwargs):
        data = get_data()
        index = find_msg(data['messages'], message_id)
        if index is None:
            raise ValueErr("Message no longer exists")
        kwargs['msg_index'] = index
        return function(token, message_id, *args, **kwargs)
    return wrapper

def check_pinned(function):
    """ decorator function for checking if the message has been pinned """
    def wrapper(token, message_id, *args, **kwargs):
        index = kwargs['msg_index']
        data = get_data()
        if data['messages'][index].is_pinned:
            raise ValueErr("Message is already pinned")
        return function(token, message_id, *args, **kwargs)
    return wrapper

def check_unpinned(function):
    """ decorator function for checking if the message has been unpinned """
    def wrapper(token, message_id, *args, **kwargs):
        index = kwargs['msg_index']
        data = get_data()
        if not data['messages'][index].is_pinned:
            raise ValueErr("Message is already pinned")
        return function(token, message_id, *args, **kwargs)
    return wrapper

def check_vuid(function):
    """ decorator function for checking if the user with u_id exists """
    def wrapper(*args, **kwargs):
        u_id = args[-1]
        data = get_data()
        if not is_user(u_id, data):
            raise ValueErr('u_id does not refer to a valid user')
        return function(*args, **kwargs)
    return wrapper

def check_vname(function):
    """ decorator function for checking if the names are in correct format """
    def wrapper(*args, **kwargs):
        # checking for length
        if not 1 < len(args[-1]) < NAME_LEN or not 1 < len(args[-2]) < NAME_LEN:
            raise ValueErr('Invalid name')
        # checking for space
        if " " in args[-1] or " " in args[-2]:
            raise ValueErr('Invalid space in names')
        return function(*args, **kwargs)
    return wrapper

def check_vemail(function):
    """ decorator function for checking if an email address is valid """
    def wrapper(*args, email, **kwargs):
        if not re.search(PATTERN, email):
            raise ValueErr('Invalid Email.')
        data = get_data()
        if any(user.email == email for user in data['users']):
            raise ValueErr('Email Exists')
        return function(*args, email, **kwargs)
    return wrapper

def check_vhandle(function):
    """ decorator function for checking if the handle is in correct format """
    def wrapper(*args, **kwargs):
        # checking if handle_str is too long/too short
        if len(args[-1]) < HANDLE_LOWER or len(args[-1]) > HANDLE_UPPER:
            raise ValueErr('Handle length not allowed.')
        return function(*args, **kwargs)
    return wrapper

def check_vcoordinates(function):
    """ decorator function for checking if the handle is in correct format """
    def wrapper(*args, **kwargs):
        x_start = args[2]
        y_start = args[3]
        x_end = args[4]
        y_end = args[5]
        # check if the given coordinates are valid
        if x_start < 0 or y_start < 0 or x_end < 0 or y_end < 0:
            raise ValueErr('Invalid coordinate')
        if x_end <= x_start or y_end <= y_start:
            raise ValueErr('Invalid coordinate')
        if (x_end - x_start) != (y_end - y_start):
            raise ValueErr('Only accept square cropping')
        return function(*args, **kwargs)
    return wrapper

def get_u_token(function):
    """ decorator function for getting a user's info """
    def wrapper(token, *args):
        data = get_data()
        if not is_session_valid(token, data):
            raise AccessError('Invalid token')
        u_id = get_user_from_token(token)['u_id']
        i = find_user(u_id, data)
        user = data['users'][i]
        return function(user, *args)
    return wrapper

def get_u_token_k(function):
    """ decorator function for getting a user's info """
    def wrapper(token, *args, **kwargs):
        data = get_data()
        if not is_session_valid(token, data):
            raise AccessError('Invalid token')
        u_id = get_user_from_token(token)['u_id']
        i = find_user(u_id, data)
        user = data['users'][i]
        kwargs['user_index'] = i
        kwargs['token'] = token
        return function(user, *args, **kwargs)
    return wrapper
