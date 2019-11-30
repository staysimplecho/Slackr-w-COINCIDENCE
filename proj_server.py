import sys
sys.path.append('./server')
import re
import random
import string
from json import dumps
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_mail import Mail, Message

from iter3 import get_data, update_data, reset_data, generate_random_string, generate_m_id
from auths import auth_register, auth_login, auth_logout, passwordreset_reset
from auths import admin_userpermission_change
from channels import channel_invite, channel_details, channel_leave
from channels import channel_join, channel_removeowner, channel_addowner
from channels import channels_list, channels_create, channels_listall
from channels import channel_messages
from messages import message_edit, message_send, message_remove, message_unpin
from messages import message_pin, message_react, message_unreact, search_message
from messages import message_sendlater
from standup import standup_start, standup_send, standup_active
from new_profile import user_profile, users_listall, user_profile_setemail, user_profile_sethandle
from new_profile import user_profiles_uploadphoto, user_profile_setname
from error_handle import AccessError, ValueErr

PATTERN = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

APP = Flask(__name__, static_folder="", static_url_path="")
CORS(APP)

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'unswcs1531@gmail.com',
    MAIL_PASSWORD = "15311531"
)

@APP.route('/auth/register', methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    base = str(request.host_url)
    host = f'{base}imgurl/default.jpg'
    try:
        info = auth_register(password, name_first, name_last, email=email, host=host)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps(info)

@APP.route('/auth/login', methods=['POST'])
def connect():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        info = auth_login(password, email=email)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps(info)

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    is_success = auth_logout(token)
    return dumps({
        'is_success': is_success
    })

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordrequest():
    mail = Mail(APP)   
    email = request.form.get('email') 
    data = get_data()
    #'reset_users': [{'u_id': 123, 'reset_code': 1231312}, {}, {}] 
    if (re.search(PATTERN, email)):
        #check if the email alr in user dict     
        if any (email in user.email for user in data['users']):
            resetcode = generate_random_string()

            msg = Message("Send Mail Test!", sender="unswcs1531@gmail.com", recipients=[email])
            msg.body = resetcode
            mail.send(msg)

            for user in data['users']:
                if(user.email == email):   
                    #if the reset_user is empty then append new item
                    if data['reset_users'] == []:
                        data['reset_users'].append({
                            'u_id': user.u_id,
                            'reset_code' : resetcode
                        })
                        update_data(data)
                        return dumps({})

                    #if not any u_id appears in the reset_user dict then add it
                    if not any(i['u_id'] == user.u_id for i in data['reset_users']):
                        print('not any')
                        data['reset_users'].append({
                            'u_id': user.u_id,
                            'reset_code' : resetcode
                        })
                        update_data(data)
                        return dumps({})

                    #check if there is match u_id, change the resetcode to latest
                    for i in data['reset_users']:
                        print(resetcode)
                        if(user.u_id == i['u_id']):
                            i['reset_code'] = resetcode
                            update_data(data)
                            return dumps({})
            return dumps({})
        return dumps({})
    else:
        return dumps({})

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def passwordreset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    try:
        passwordreset_reset(new_password, reset_code)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps({})

@APP.route('/channel/invite', methods=['POST'])
def invite():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    u_id = request.form.get('u_id', type=int)
    try:
        _ = channel_invite(token, channel_id, u_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/channel/details', methods=['GET'])
def details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', type=int)
    try:
        info = channel_details(token, channel_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps(info)

@APP.route('/channel/leave', methods=['POST'])
def leave():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    try:
        _ = channel_leave(token, channel_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/channel/join', methods=['POST'])
def join():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    try:
        _ = channel_join(token, channel_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/channel/removeowner', methods=['POST'])
def remove_owner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    u_id = request.form.get('u_id', type=int)
    try:
        _ = channel_removeowner(token, channel_id, u_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/channel/addowner', methods=['POST'])
def add_owner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    u_id = request.form.get('u_id', type=int)
    try:
        _ = channel_addowner(token, channel_id, u_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/channels/list', methods=['GET'])
def list_channel():
    token = request.args.get('token')
    channels = channels_list(token)
    return dumps({
            "channels": channels
        })

@APP.route('/channels/create', methods=['POST'])
def channel_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    if is_public == 'true':
        is_public = True
    else:
        is_public = False
    try:
        info = channels_create(token, name, is_public)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps(info)

@APP.route('/channels/listall', methods=['GET'])
def listinfo():
    token = request.args.get('token')
    channels = channels_listall(token)
    return dumps({
        'channels': channels
    })

@APP.route('/channel/messages', methods=['GET'])
def load_msg():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', type=int)
    start = request.args.get('start', type=int)
    try:
        info = channel_messages(token, channel_id, start)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps(info)

@APP.route('/message/send', methods=['POST'])
def send_msg():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    message = request.form.get('message')
    try:
        message_id = message_send(token, channel_id, message)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))

    return dumps({
        'message_id': message_id
    })

@APP.route('/message/remove', methods=['DELETE'])
def remove_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    try:
        _ = message_remove(token, message_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/message/edit', methods=['PUT'])
def edit_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    message = request.form.get('message')
    try:
        _ = message_edit(token, message_id, message)
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/message/react', methods=['POST'])
def react_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    react_id = request.form.get('react_id', type=int)
    try:
        _ = message_react(token, message_id, react_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps({})

@APP.route('/message/unreact', methods=['POST'])
def unreact_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    react_id = request.form.get('react_id', type=int)
    try:
        _ = message_unreact(token, message_id, react_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps({})

@APP.route('/message/pin', methods=['POST'])
def pin_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    try:
        _ = message_pin(token, message_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/message/unpin', methods=['POST'])
def unpin_msg():
    token = request.form.get('token')
    message_id = request.form.get('message_id', type=int)
    try:
        _ = message_unpin(token, message_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/user/profile', methods=['GET'])
def get_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id', type=int)

    try:
        info = user_profile(token, u_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps(info)

@APP.route('/user/profiles/uploadphoto', methods=['POST'])  
def upload_photo():
    token = request.form.get('token')
    img_url = request.form.get('img_url')    
    x_start = request.form.get('x_start', type=int)
    y_start = request.form.get('y_start', type=int)
    x_end = request.form.get('x_end', type=int)
    y_end = request.form.get('y_end', type=int)
    host = str(request.host_url)
    try:
        _ = user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, host)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps({})

@APP.route('/users/all', methods=['GET'])
def all_users():
    token = request.args.get('token')
    user = users_listall(token)
    return dumps({
            "users": user
    })

@APP.route('/standup/start', methods=['POST'])
def s_start():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id',type=int)
    length = request.form.get('length',type=int)
    try:
        finish_time = standup_start(token, channel_id, length)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({
        'time_finish': finish_time
    })

@APP.route('/standup/send', methods=['POST'])
def s_send():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    message = request.form.get('message')
    try:
        standup_send(token, channel_id, message)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))
    return dumps({})

@APP.route('/user/profile/setname', methods=['PUT'])
def reset_name():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    print(name_first)
    try:
        _ = user_profile_setname(token, name_first, name_last)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps({})

@APP.route('/user/profile/setemail', methods=['PUT'])
def reset_email():
    token = request.form.get('token')
    email = request.form.get('email')
    try:
        info = user_profile_setemail(token, email=email)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps(info)

@APP.route('/user/profile/sethandle', methods=['PUT'])  
def reset_handle():
    token = request.form.get('token')
    handle = request.form.get('handle')
    try:
        info = user_profile_sethandle(token, handle)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    return dumps(info)

@APP.route('/search', methods=['GET'])
def search():
    token = request.args.get('token')
    string = request.args.get('query_str')
    message = search_message(token, string)
    return dumps({
        'messages': message
    })

@APP.route('/admin/userpermission/change', methods = ['POST'])
def changepermission():
    token = request.form.get('token')
    u_id = request.form.get('u_id', type=int)
    permission_id = request.form.get('permission_id', type=int) 
    try:
        admin_userpermission_change(token, permission_id, u_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))   
    return dumps({})    

@APP.route('/message/sendlater', methods=['POST'])
def s_later():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id', type=int)
    message = request.form.get('message')
    time_sent = request.form.get('time_sent', type=float)

    try:
        message_id = message_sendlater(token, channel_id, message, time_sent)
    except ValueErr as e:
        raise ValueErr(description=str(e))
    except AccessError as e:
        raise AccessError(description=str(e))

    return dumps({
        'message_id': message_id
    })

@APP.route('/standup/active', methods=['GET'])
def standup_state():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', type=int)
    try:
        state, finish_time = standup_active(token, channel_id)
    except ValueErr as e:
        raise ValueErr(description=str(e))

    return dumps({
        'is_active': state,
        'time_finish': finish_time
    })

if __name__ == '__main__':
    '''
    reset_data() is reserved for testing initialization
    PLEASE comment the line out when the App is ready for releasing
    '''
    # reset_data()
    APP.run(debug=True, port=(sys.argv[1] if len(sys.argv) > 1 else 5009))
