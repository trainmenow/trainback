from flask import request
from flask_restx import Resource

from trainback.trainlog.workout import api

from trainback.trainmanager.auth.decorators import admin_required, user_required


@api.route('/')
class Workouts(Resource):
    @api.doc('list of all workouts', security='jwt')
    @user_required
    def get(self):
        pass
    
    @api.doc('create a new workout', security='jwt')
    @user_required
    def post(self):
        pass


@api.route('/<workout_id>')
@api.param('workout_id', 'The workout identifier')
class SingleWorkout(Resource):
    @api.doc('detailed information of one workout', security='jwt')
    @user_required
    def get(self):
        pass
    
    @api.doc('update a workout', security='jwt')
    @user_required
    def put(self):
        pass
    
    @api.doc('delete a workout', security='jwt')
    @user_required
    def delete(self):
        pass