from flask import request
from flask_restplus import Resource

from trainback.trainmanager.user_account import api
from flask_jwt_extended import get_jwt_identity
from trainback.trainmanager.auth.decorators import admin_required, user_required

from trainback.trainmanager.user_account.dto import AccountDto
from trainback.trainmanager.auth.dto import TokenDto
from trainback.trainmanager.user_account.parser import (
    user_account_parser, user_credentials_parser, account_names_parser, change_password_parser,
    new_password_parser, useroremail_parser )

from trainback.trainmanager.user_account.service import create, get, update_names, delete_user, get_all, login, verify, change_password, request_password, new_password


_account = AccountDto.account
_token = TokenDto.token

@api.route('/')
class AccountList(Resource):
    @api.doc('list of all users', security='jwt')
    @api.marshal_list_with(_account, envelope='data')
    @user_required
    def get(self):
        return get(get_jwt_identity())

    @api.doc('create a new user')
    @api.response(201, 'User successfully created.')
    @api.expect(user_account_parser) # @api.expect(user_account_parser, validate=True)
    def post(self):
        data = user_account_parser.parse_args(request)
        return create(data)

    @api.doc('update names of user', security='jwt')
    @user_required
    @api.expect(account_names_parser)
    @api.response(202, 'User successfully updated.')
    def put(self):
        data = account_names_parser.parse_args(request)
        return update_names(get_jwt_identity(), data)

    @api.doc('delete user', security='jwt')
    @user_required
    @api.response(205, 'User successfully deleted.')
    def delete(self):
        return delete_user(get_jwt_identity())


@api.route('/login')
class Login(Resource):
    @api.doc('login as user')
    @api.expect(user_credentials_parser)
    @api.marshal_with(_token)
    def post(self):
        data = user_credentials_parser.parse_args(request)
        return login(data)


# @api.route('/<public_id>')
# @api.param('public_id', 'The User Account identifier')
# class PublicAccount(Resource):
#     @api.doc('get user information')
#     @api.marshal_with(_account)
#     def get(self):
#         pass


@api.route('/all')
class AllAccounts(Resource):
    @api.doc('list of all users', security='admin')
    @admin_required
    @api.marshal_list_with(_account, envelope='users')
    def get(self):
        return get_all()


@api.route('/verify/<code>')
@api.param('code', 'The User Account verification code')
class Verify(Resource):
    @api.doc('verify your account')
    @api.response(201, 'User successfully activated.')
    def get(self, code):
        return verify(code)


@api.route('/password')
class Password(Resource):
    @api.doc('change your password', security='jwt')
    @user_required
    @api.expect(change_password_parser)
    @api.response(200, 'Password successfully updated.')
    def put(self):
        data = change_password_parser.parse_args(request)
        return change_password(get_jwt_identity(), data)


@api.route('/password/forgotten')
class PasswordReset(Resource):
    @api.doc('request a code to reset your password')
    @api.expect(useroremail_parser)
    @api.response(200, 'Email has been sent.')
    def post(self):
        data = useroremail_parser.parse_args(request)
        return request_password(data)


@api.route('/password/<code>')
@api.param('code', 'The User Account password reset code')
class PasswordResetCode(Resource):
    @api.doc('set a new password')
    @api.expect(new_password_parser)
    @api.response(200, 'Password successfully updated.')
    def put(self, code):
        data = new_password_parser.parse_args(request)
        return new_password(code, data)