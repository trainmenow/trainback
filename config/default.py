import os

SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
DEBUG = False