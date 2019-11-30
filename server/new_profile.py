#pylint: disable-msg=too-many-arguments
#pylint: disable-msg=too-many-locals
#pylint: disable-msg=unused-argument
'''
This file includes functions on profile modification.
'''
import os
from io import BytesIO
from PIL import Image
import requests
from iter3 import get_data, update_data
from iter3 import find_user, handle_exists
from error_handle import ValueErr
import all_decos as deco

@deco.check_vtoken
def user_profile(u_id):
    """ Function for getting a user's profile details """
    data = get_data()
    i = find_user(u_id, data)
    if i is None:
        raise ValueErr("User with u_id is not a valid user")

    return {
        'email': data['users'][i].email,
        'name_first': data['users'][i].name_first,
        'name_last': data['users'][i].name_last,
        'handle_str': data['users'][i].handle,
        'profile_img_url': data['users'][i].img_url
    }

@deco.check_vtoken
def users_listall():
    '''
    list all the users in the slackr
    '''
    data = get_data()
    new_list = []
    for user in data['users']:
        new = {
            'u_id': user.u_id,
            'email': user.email,
            'name_first': user.name_first,
            'name_last': user.name_last,
            'handle_str': user.handle,
            'profile_img_url': user.img_url
        }
        new_list.append(new)
    return new_list

@deco.get_u_token_k
@deco.check_vname
def user_profile_setname(user, name_first, name_last, **kwargs):
    """ Function for resetting user's name """
    # reset names
    data = get_data()
    index = kwargs['user_index']
    data['users'][index].reset_names(name_first, name_last)
    update_data(data)
    return {}

@deco.get_u_token_k
@deco.check_vemail
def user_profile_setemail(user, email, **kwargs):
    """ Function for resetting user's email """
    data = get_data()
    # reset email
    index = kwargs['user_index']
    data['users'][index].reset_email(email)
    update_data(data)
    return {}


@deco.get_u_token_k
@deco.check_vhandle
def user_profile_sethandle(user, handle_str, **kwargs):
    """ Function for resetting user's handle """
    data = get_data()
    handle_str = str.lower(handle_str)
    # checking if same handle has been registered already or not
    if handle_exists(handle_str, data):
        raise ValueErr('Handle already exists.')

    index = kwargs['user_index']
    data['users'][index].reset_handle(handle_str)
    update_data(data)
    return {}

@deco.get_u_token_k
@deco.check_vcoordinates
def user_profiles_uploadphoto(user, img_url, x_start, y_start,
                              x_end, y_end, host, **kwargs):
    """ Function for setting/updating a user's profile photo """
    data = get_data()
    # grab the online JPG/JPEG image
    # - request status
    try:
        res = requests.get(img_url)
    except:
        raise ValueErr('Invalid URL')
    if res.status_code != 200:
        raise ValueErr('Unable to get content')
    # - image format
    try:
        img = Image.open(BytesIO(res.content))
    except OSError:
        raise ValueErr('Unable to identify image file')
    if img.format != 'JPG' and img.format != 'JPEG':
        raise ValueErr('Image uploaded is not a JPG')
    # - square cropping
    img_w, img_h = img.size
    if x_end > img_w or y_end > img_h:
        raise ValueErr('Invalid coordinate')
    # crop the image
    box = (x_start, y_start, x_end, y_end)
    cropped = img.crop(box)

    # check existence of the local static directory
    if not os.path.isdir('./imgurl'):
        os.mkdir('./imgurl')
    # save the image locally
    cwd = os.path.dirname(__file__)
    rel_path = f"../imgurl/{user.u_id}_avatar.jpg"
    local_url = os.path.join(cwd, rel_path)
    cropped.save(local_url)

    # save the image in server/database
    server_url = f"{host}imgurl/{user.u_id}_avatar.jpg"
    index = kwargs['user_index']
    data['users'][index].add_avatar(server_url)
    update_data(data)
    return server_url
