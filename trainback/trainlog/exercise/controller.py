from flask import request
from flask_restx import Resource

from trainback.trainlog.exercise import api
from trainback.trainlog.service import get_exercises, create_exercise
from trainback.trainlog.exercise.dto import ExerciseDto
from trainback.trainlog.exercise.parser import exercise_parser

from trainback.trainmanager.auth.decorators import admin_required, user_required

_exercise = ExerciseDto.exercise

@api.route('/')
class Exercises(Resource):
    @api.doc('list of all exercises')
    @api.marshal_list_with(_exercise, envelope='exercises', skip_none=True)
    def get(self):
        return get_exercises()
    
    @api.doc('create a new workout', security='jwt')
    # @user_required
    @api.expect(exercise_parser)
    def post(self):
        data = exercise_parser.parse_args(request)
        return create_exercise(data.exercise)