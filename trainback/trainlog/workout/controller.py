from flask import request
from flask_restx import Resource
from flask_jwt_extended import get_jwt_identity

from trainback.trainlog.workout import api
from trainback.trainlog.service import create_workout, get_workouts_by_user, get_workout_by_id, del_workout_by_id, replace_workout
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
    @api.marshal_with(_workout, skip_none=True)
    def get(self, workout_id):
        return get_workout_by_id(workout_id, get_jwt_identity())
    
    @api.doc('update a workout', security='jwt')
    @user_required
    @api.expect(workout_parser)
    def put(self, workout_id):
        data = workout_parser.parse_args(request)
        return replace_workout(workout_id, get_jwt_identity(), data.workout)
    
    @api.doc('delete a workout', security='jwt')
    @user_required
    def delete(self, workout_id):
        return del_workout_by_id(workout_id, get_jwt_identity())