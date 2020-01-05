from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('logger_api', __name__, url_prefix='/log')

api = Api(blueprint,
          title='TRAINBACK LOGGER API',
          version='0.1',
          description='an api logging training sessions and foofplans'
          )

# api.add_namespace()