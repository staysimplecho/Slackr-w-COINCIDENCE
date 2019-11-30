'''
This file stores all authentication and authorization related function
'''
from error_handle import AccessError, ValueErr
from iter3 import User
from iter3 import get_data, update_data
from iter3 import generate_id, generate_token, hash_password, find_user
from iter3 import is_session_valid, handle_exists
from all_decos import check_vuid, check_vemail, check_vname,\
check_vpassword, get_u_token

# GLOBAL VALUE BELOW
PATTERN = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
SEED = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
SLACKR_OWNER = 1
SLACKR_ADMIN = 2
SLACKR_USER = 3
PW_LENGTH = 6
HANDLE_LEN = 20
MODIFIED_LEN = 18
# GLOBAL VALUE ABOVE

@check_vname
@check_vemail
@check_vpassword
def auth_register(password, name_first, name_last, email, **kwargs):
    """
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for authentication
    in their session.
    """
    data = get_data()

    _list = [user.u_id for user in data['users']]
    u_id = generate_id(_list)
    # handle must be in lower case
    handle = str.lower(name_first) + str.lower(name_last)
    # handle length no longer than 20 characters
    if len(handle) > HANDLE_LEN:
        handle = handle[0:HANDLE_LEN]

    # if the handle already exist
    suffix = 0
    while handle_exists(handle, data):
        suf_str = f'{suffix}'
        suf_len = len(suf_str)
        # make sure that the patched handle won't exceed HANDLE_LEN
        if len(handle) + suf_len <= HANDLE_LEN:
            handle += suf_str
        else:
            base_len = HANDLE_LEN - len(suf_str)
            handle = handle[0:base_len] + suf_str
        suffix += 1

    # registered user is by default slackr user
    permission_id = SLACKR_USER
    # first registered is the owner of slackr
    if data['users'] == []:
        permission_id = SLACKR_OWNER
    # default profile photo
    host = None
    if 'host' in kwargs: 
        host = kwargs['host']
    user = User(u_id, email, hash_password(password),
                name_first, name_last, handle, permission_id, host)
    data['users'].append(user)
    token = generate_token(email, u_id, name_first, name_last)
    data['login_users'].append(token)
    update_data(data)
    return {
        'u_id': u_id,
        'token': token
    }

def auth_login(password, email):
    """
    Given a registered users' email and password and generates a
    valid token for the user to remain authenticated
    """
    data = get_data()
    if not any(email == user.email for user in data['users']):
        raise ValueErr('Email has not been register')
    for user in data['users']:
        if user.email == email and user.password == hash_password(password):
            newtoken = generate_token(email, user.u_id, user.name_first,
                                      user.name_last)
            data['login_users'].append(newtoken)
            update_data(data)
            return {
                'u_id': user.u_id,
                'token': newtoken
            }
    raise ValueErr("Incorrect Password")

def auth_logout(token):
    """
    Given an active token, invalidates the taken to log the user out.
    """
    data = get_data()
    if is_session_valid(token, data):
        data['login_users'].remove(token)
        update_data(data)
        return True
    return False

def passwordreset_request(email):
    """
    password_reset_request function placeholder
    """
    print(email)
    data = get_data()
    return data

@check_vpassword
def passwordreset_reset(new_password, reset_code):
    """
    Given a reset code for a user, set that user's new
    password to the password provided
    """
    data = get_data()

    # find corespond user and change password
    for user in data['reset_users']:
        if user['reset_code'] == reset_code:
            index = find_user(user['u_id'], data)
            data['users'][index].reset_password(new_password)
            update_data(data)
            return {}
    # reset_code wasn't found
    raise ValueErr('Invalid reset_code')

@get_u_token
@check_vuid
def admin_userpermission_change(user, permission_id, u_id):
    """
    Given a User by their user ID, set their permissions
    to new permissions described by permission_id
    """
    data = get_data()
    #get u_id info from token
    #u_id for the people who change
    user_id = user.u_id
    #permission id for the people who change
    user_perm = user.permission_id

    if user_id == u_id:
        raise ValueErr('user cannot change permission for himself')

    if permission_id not in (SLACKR_OWNER, SLACKR_ADMIN, SLACKR_USER):
        raise ValueErr('permission_id not refer to a valid permission')

    index = find_user(u_id, data)
    target_user = data['users'][index]
    if user_perm == SLACKR_USER:
        raise AccessError('the authorised user is not admin or owner')

    if (user_perm == SLACKR_ADMIN and target_user.permission_id == SLACKR_OWNER):
        raise AccessError('Admin cannot change permission for slackr owner')
    if user_perm == SLACKR_ADMIN and permission_id == SLACKR_OWNER:
        raise AccessError('Admin cannot promote slackr owners')
    target_user.permission_id = permission_id
    update_data(data)
    return {}
