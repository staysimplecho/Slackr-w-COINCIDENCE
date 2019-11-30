'''
This file is to test user_profiles uploadphoto
Given a URL of an image on the internet, crops the image within bounds\
(x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
'''

#pylint: disable-msg=too-many-function-args
#pylint: disable-msg=invalid-name
import pytest
from iter3 import get_data, get_user_from_token, find_user, reset_data
from auths import auth_register
from error_handle import ValueErr
from new_profile import user_profiles_uploadphoto


VALID_URL = 'https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_960_720.jpg'
INVALID_URL = 'a'
GHOST_PAGE = 'http://xingjiangminghu.lofter.com/'
NOT_IMAGE = 'http://mumofuronghua.lofter.com/post/251454_f3fa88b'
PNG_IMAGE = 'https://cdn.shopify.com/s/files/1/1061/1924/files/Eye_Roll_Emoji_large.png'

def test_user_photo_success():
    """
    This function tests for a successful upload of photo
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    info = get_user_from_token(token)
    u_id = info['u_id']
    user_profiles_uploadphoto(token, VALID_URL, 0, 0, 10, 10,
                              'http://127.0.0.1:5001/')
    data = get_data()
    index = find_user(u_id, data)
    assert data['users'][index].img_url == f"http://127.0.0.1:5001/imgurl/{u_id}_avatar.jpg"

def test_INVALID_URL():
    """
    This function tests for a failed upload of photo
    (invalid url provided)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, INVALID_URL, 0, 0, 10, 10,
                                  'http://127.0.0.1:5001/')

def test_page_doesnt_exist():
    """
    This function tests for a failed upload of photo
    (status code is not 200)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, GHOST_PAGE, 0, 0, 10, 10,
                                  'http://127.0.0.1:5001/')

def test_not_an_image():
    """
    This function tests for a failed upload of photo
    (url does not lead to an image file)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, NOT_IMAGE, 0, 0, 10, 10,
                                  'http://127.0.0.1:5001/')

def test_invalid_format():
    """
    This function tests for a failed upload of photo
    (invalid format)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, PNG_IMAGE, 0, 0, 10, 10,
                                  'http://127.0.0.1:5001/')

def test_photo_negative_coordinate():
    """
    This function tests for a failed upload of photo
    (x_end out of bound)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, VALID_URL, -100, 0, 10, 10,
                                  'http://127.0.0.1:5001/')

def test_photo_invalid_coordinate():
    """
    This function tests for a failed upload of photo
    (x_end <= x_start)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, VALID_URL, 10, 0, 0, 10,
                                  'http://127.0.0.1:5001/')

def test_not_square():
    """
    This function tests for a failed upload of photo
    (not square cropping)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, VALID_URL, 0, 0, 10, 15,
                                  'http://127.0.0.1:5001/')

def test_photo_out_of_Range():
    """
    This function tests for a failed upload of photo
    (cropping size out of bound)
    """
    reset_data()
    userDic = auth_register('12345678', 'Vivian', 'VVV', email='1a@gmail.com')
    token = userDic['token']
    with pytest.raises(ValueErr):
        user_profiles_uploadphoto(token, VALID_URL, 0, 0, 50000, 50000,
                                  'http://127.0.0.1:5001/')
