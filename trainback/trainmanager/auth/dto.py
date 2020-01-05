from flask_restplus import fields
from trainback.trainmanager.auth import api


class TokenDto:
    token = api.model('token', {
        'error': fields.Boolean(default=False, description=''),
        'message': fields.String(description='message'),
        'access_token': fields.String(description='access token for authorization'),
        'refresh_token': fields.String(description='refresh token')
    })