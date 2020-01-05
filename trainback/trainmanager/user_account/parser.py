from flask_restplus import reqparse


user_account_parser = reqparse.RequestParser()
user_account_parser.add_argument('username', type=str, required=True, help='username')
user_account_parser.add_argument('email', type=str, required=True, help='email')
user_account_parser.add_argument('password', type=str, required=True, help='password')
user_account_parser.add_argument('firstname', type=str, help='firstname')
user_account_parser.add_argument('lastname', type=str, help='lastname')


user_credentials_parser = reqparse.RequestParser()
user_credentials_parser.add_argument('user', type=str, required=True, help='username or email')
user_credentials_parser.add_argument('password', type=str, required=True, help='password')


account_names_parser = reqparse.RequestParser()
account_names_parser.add_argument('firstname', type=str, help='firstname')
account_names_parser.add_argument('lastname', type=str, help='lastname')


change_password_parser = reqparse.RequestParser()
change_password_parser.add_argument('old_password', type=str, required=True, help='password')
change_password_parser.add_argument('new_password', type=str, required=True, help='password')


new_password_parser = reqparse.RequestParser()
new_password_parser.add_argument('password', type=str, required=True, help='password')


useroremail_parser = reqparse.RequestParser()
useroremail_parser.add_argument('user', type=str, help='username or email')