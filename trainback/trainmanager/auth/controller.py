from flask import request
from flask_restx import Resource

from trainback.trainmanager.auth import api
from flask_jwt_extended import jwt_refresh_token_required, jwt_required

from trainback.trainmanager.auth.dto import TokenDto
from trainback.trainmanager.auth.models import RevokedTokenModel

from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, get_raw_jwt


_token = TokenDto.token


@api.route('/token/refresh')
class RefreshToken(Resource):
    @api.doc('refresh access token', security='jwt-refresh')
    @jwt_refresh_token_required
    @api.marshal_with(_token)
    def get(self):
        jti = get_raw_jwt()['jti']
        if RevokedTokenModel.is_jti_blacklisted(jti=jti):
            return {'error': True, 'message':'Your token has been revoked!'}, 401

        identity = get_jwt_identity()
        claims = get_jwt_claims()
        access_token = create_access_token(identity = identity, user_claims=claims)
        return {'message': 'Created new access token.', 'access_token': access_token}


@api.route('/token/revoke')
class RevokeToken(Resource):
    @api.doc('revoke access token', security='jwt')
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500

@api.route('/token/revoke/refresh')
class RevokeRefreshToken(Resource):
    @api.doc('revoke refresh token', security='jwt-refresh')
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}, 200
        except:
            return {'message': 'Something went wrong'}, 500