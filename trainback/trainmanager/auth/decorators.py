from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, get_jti, get_raw_jwt

from trainback import jwt
from trainback.trainmanager.auth.models import RevokedTokenModel


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if check_if_token_in_blacklist(get_raw_jwt()):
            return {'error': True, 'message':'Your token has been revoked!'}, 401
        if claims['role'] != 'admin':
            return {'error': True, 'message':'You have no admin permissions!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if check_if_token_in_blacklist(get_raw_jwt()):
            return {'error': True, 'message':'Your token has been revoked!'}, 401
        if claims['role'] != 'user':
            return {'error': True, 'message':'You have no permissions for that!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper



@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    jti = token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti=jti)