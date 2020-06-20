from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('chat_api', __name__, url_prefix='/chat')

api = Api(blueprint,
          title='TRAINBACK CHAT API',
          version='0.1',
          description='an api for chatting'
          )

# api.add_namespace()