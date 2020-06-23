from flask import request
from flask_restx import Resource
# from bson.objectid import ObjectId
from flask_jwt_extended import get_jwt_identity

from trainback.trainlog.workout import api
from trainback.trainlog.service import create_workout, get_workouts_by_user
from trainback.trainlog.workout.parser import workout_parser
from trainback.trainlog.workout.dto import WorkoutDto

from trainback.trainmanager.auth.decorators import admin_required, user_required

_workout = WorkoutDto.workout

@api.route('/')
class Workouts(Resource):
    @api.doc('list of all workouts of a user', security='jwt')
    @user_required
    @api.marshal_list_with(_workout, envelope='workouts', skip_none=True)
    def get(self):
        return get_workouts_by_user(get_jwt_identity())
    
    @api.doc('create a new workout', security='jwt')
    @user_required
    @api.expect(workout_parser)
    def post(self):
        data = workout_parser.parse_args(request)
        return create_workout(data.workout, get_jwt_identity())


@api.route('/<ObjectId:workout_id>')
@api.param('workout_id', 'The workout identifier')
class SingleWorkout(Resource):
    @api.doc('detailed information of one workout', security='jwt')
    @user_required
    def get(self, workout_id):
        pass
    
    @api.doc('update a workout', security='jwt')
    @user_required
    def patch(self, workout_id):
        pass
    
    @api.doc('delete a workout', security='jwt')
    @user_required
    def delete(self, workout_id):
        pass