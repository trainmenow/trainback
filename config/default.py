import os

SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
FLASK_THREADED = True
DEBUG = False

SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

MAIL_DEFAULT_SENDER = 'noreply@trainmenow.de'

# JWT_BLACKLIST_ENABLED = True
# JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']