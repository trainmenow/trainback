import uuid
from datetime import datetime, timedelta

from trainback import db, jwt, mail
from trainback.trainmanager.user_account.models import Account, Code

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_mail import Message


EMAIL_VERIFY_CODE = 1
PASSWORD_RESET_CODE = 2


def create(data):
    user = Account.query.filter_by(email=data['email']).first()
    if user:
        response_object = {
            'error': 'true',
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

    user = Account.query.filter_by(username=data['username']).first()
    if user:
        response_object = {
            'error': 'true',
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

    pubid = str(uuid.uuid4())
    user = Account.query.filter_by(public_id=pubid).first()
    while user:
        pubid = str(uuid.uuid4())
        user = Account.query.filter_by(public_id=pubid).first()

    new_user = Account(
        public_id=pubid,
        username=data['username'],
        email=data['email'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        password=data['password']
    )

    save(new_user)
    send_verify_mail(new_user)
    response_object = {
            'error': 'false',
            'status': 'success',
            'message': 'Successfully registered.',
        }
    return response_object, 201


def login(data):
    user = Account.query.filter_by(username=data['user']).first()
    if not user:
        user = Account.query.filter_by(email=data['user']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': True, 'message': 'Invalid username or password'}

    if not user.activated:
        return {'error': True, 'message': 'Please verify your account first'}
    
    if user.blocked:
        return {'error': True, 'message': 'Your account has been blocked'}

    access_token = create_access_token(identity = user.public_id, user_claims={'role': 'user'})
    refresh_token = create_refresh_token(identity = user.public_id, user_claims={'role': 'user'})
    return {
            'message': 'Logged in as {}'.format(user.username),
            'access_token': access_token,
            'refresh_token': refresh_token
        }


def get(public_id):
    user = Account.query.filter_by(public_id=public_id).first_or_404()
    return user


def update_names(public_id, names):
    user = Account.query.filter_by(public_id=public_id).first()
    user.firstname = names['firstname']
    user.lastname = names['lastname']
    update()
    return {'error': False, 'message': 'User has been updated', 'test': public_id}, 201


def delete_user(public_id):
    user = Account.query.filter_by(public_id=public_id).first_or_404()
    delete(user)
    return {'error': False, 'message': 'User has been deleted'}, 205


def verify(codestring):
    code = Code.query.filter_by(code=codestring).first()
    if not code or not code.purpose == EMAIL_VERIFY_CODE:
        return {'error': True, 'message': 'Your code is incorrect'}
    if datetime.now() >= code.created + timedelta(hours=24):
        return {'error': True, 'message': 'Your code expired'}
    user = Account.query.filter_by(public_id=code.user).first()
    if not user:
        return {'error': True, 'message': 'User doesn\'t exist'}
    delete(code)
    user.activated = True
    update()
    return {'error': False, 'message': 'User has been activated'}


def change_password(public_id, data):
    user = Account.query.filter_by(public_id=public_id).first()
    if not user:
        return {'error': True, 'message': 'Identity not found.'}, 404
    if not user.check_password(data['old_password']):
        return {'error': True, 'message': 'Password incorrect.'}, 401
    user.password = data['new_password']
    update()

    return {'error': False, 'message': 'Password successfully updated.'}, 200


def request_password(data):
    user = Account.query.filter_by(username=data['user']).first()
    if not user:
        user = Account.query.filter_by(email=data['user']).first()
    if not user:
        return {'error': True, 'message': 'Username or Email doesn\'t exist.'}, 404
    send_password_mail(user)
    return {'error': False, 'message': 'Email has been sent.'}, 200


def new_password(codestring, data):
    code = Code.query.filter_by(code=codestring).first()
    if not code or not code.purpose == PASSWORD_RESET_CODE:
        return {'error': True, 'message': 'Your code is incorrect'}
    if datetime.now() >= code.created + timedelta(hours=24):
        return {'error': True, 'message': 'Your code expired'}
    user = Account.query.filter_by(public_id=code.user).first()
    if not user:
        return {'error': True, 'message': 'User doesn\'t exist'}
    delete(code)
    user.password = data['password']
    update()
    return {'error': False, 'message': 'Password successfully updated.'}, 200


# ~~~~~~~~ Intern Functions ~~~~~~~~


def send_verify_mail(userObject):
    code = create_verify_code(userObject.public_id)
    msg = Message("Registrierung abschließen")
    msg.add_recipient(userObject.email)

    msg.body = """Hey {},
    Herzlich Willkommen bei trainmenow.de
    
    Du bist nurnoch einen Schritt von deinem ersten Training entfernt.
    Klicke auf den unten stehenden Link oder kopiere ihn in deinen Browser, um deine E-Mail Adresse zu bestätigen:
    
    https://trainmenow.de/manager/user/account/verify/""".format(userObject.username) + code

    msg.html = """Hey {},<br>
    Herzlich Willkommen bei <b>trainmenow.de</b><br>
    <br>
    Du bist nurnoch einen Schritt von deinem ersten Training entfernt.<br>
    Klicke auf das unten stehende Feld, um deine E-Mail Adresse zu bestätigen:<br>
    <br>
    <a href="https://trainmenow.de/manager/user/account/verify/""".format(userObject.username) + code + """">Bestätigen</a><br>
    <br>
    <i>Solltest du dich nicht registriert haben, kannst du diese Nachricht ignorieren.</i>"""

    mail.send(msg)


def send_password_mail(userObject):
    code = create_password_code(userObject.public_id)
    msg = Message('Passwort zurücksetzen')
    msg.add_recipient(userObject.email)

    msg.body = """Benutzername: {},

    Um dein Passwort zurückzusetzen, klicke auf den folgenden Link:
    https://trainmenow.de/manager/user/account/password/""".format(userObject.username) + code

    mail.send(msg)


def create_verify_code(user):
    new_code = Code(
        user=user,
        code=get_unique_code(),
        purpose=EMAIL_VERIFY_CODE
    )
    save(new_code)
    return new_code.code


def create_password_code(user):
    new_code = Code(
        user=user,
        code=get_unique_code(),
        purpose=PASSWORD_RESET_CODE
    )
    save(new_code)
    return new_code.code


def get_unique_code():
    uniquecode = str(uuid.uuid4())
    code = Code.query.filter_by(code=uniquecode).first()
    while code:
        uniquecode = str(uuid.uuid4())
        code = Code.query.filter_by(code=uniquecode).first()
    return uniquecode


def get_all():
    return Account.query.all()


def get_by_public_id(public_id):
    return Account.query.filter_by(public_id=public_id).first()


def save(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()