from flask_restplus import fields
from trainback.trainmanager.user_account import api


class AccountDto:
    account = api.model('user account', {
        'error': fields.Boolean(default=False, description=''),
        'message': fields.String(description='message'),
        'public_id': fields.String(description='user identifier', example='729528d3-a7d3-4fef-9004-056919d97a5b'),
        'username': fields.String(required=True, description='username'),
        'email': fields.String(required=True, description='user email address'),
        'activated':fields.Boolean(description='user account activation status'),
        'blocked':fields.Boolean(description='user account blocked status'),
        'firstname': fields.String(description='user firstname'),
        'lastname': fields.String(description='user lastname'),
        'registered': fields.DateTime(description='user registration date')
    })