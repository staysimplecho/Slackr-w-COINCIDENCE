"""
Wrappers for HTTPExceptions
"""
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    ''' wrapper of AccessError for HTTPException '''
    code = 400
    message = 'No message specified'

class ValueErr(HTTPException):
    ''' wrapper of ValueError for HTTPException '''
    code = 400
    message = 'No message specified'
