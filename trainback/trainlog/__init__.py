from flask import Blueprint
from flask_restx import Api

from trainback.trainlog.workout.controller import api as workout_ns
from trainback.trainlog.exercise.controller import api as exercise_ns

blueprint = Blueprint('logger_api', __name__, url_prefix='/log')

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
          title='TRAINBACK LOGGER API',
          version='0.1',
          description='an api logging training sessions and foodplans',
          authorizations=authorizations
          )

api.add_namespace(workout_ns, path='/workout')
api.add_namespace(exercise_ns, path='/exercise')