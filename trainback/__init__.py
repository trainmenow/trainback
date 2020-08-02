from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_cors import CORS

from config import config_by_name


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
mongo = PyMongo()
cors = CORS()


from trainback.trainmanager import blueprint as manager_bp
from trainback.trainlog import blueprint as logger_bp
from trainback.trainshop import blueprint as shop_bp
from trainback.trainchat import blueprint as chat_bp


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    flask_bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    cors.init_app(app)

    app.register_blueprint(manager_bp)
    app.register_blueprint(logger_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(chat_bp)

    return app