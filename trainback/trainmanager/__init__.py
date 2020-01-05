from flask import Blueprint
from flask_restplus import Api

from trainback.trainmanager.user_account.controller import api as ua_ns
from trainback.trainmanager.auth.controller import api as auth_ns


blueprint = Blueprint('manager_api', __name__, url_prefix='/manager')

authorizations = {
    '-- How to Authorize --': {
        'type': 'apiKey',
        'name': 'Write the following in the field:',
        'in': '"Bearer + [yourJWT-Token]"'
    },
    'jwt': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    },
    'jwt-refresh': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    },
    'admin': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }}
api = Api(blueprint,
          title='TRAINBACK MANAGER API',
          version='0.1',
          description='an api for managing all accounts and profile related stuff',
          authorizations=authorizations
          )

api.add_namespace(ua_ns, path='/user/account')
api.add_namespace(auth_ns, path='/auth')