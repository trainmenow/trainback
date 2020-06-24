from flask_restx import fields
from trainback.trainlog.workout import api


class WorkoutDto:
    sets = api.model('sets', {
        'kind': fields.String(description='kind of the set'),
        'repeats': fields.Integer(description='reps'),
        'weight': fields.Float(description='weight'),
        'distance': fields.Float(description='i.e. how far u ran'),
        'time': fields.Float(description='i.e. how long u ran'),
        'pause': fields.Float(description='pause before the next set starts'),
    })

    exercise = api.model('exercise', {
        'exercise': fields.String(description='exerciseID'),
        'sets': fields.List(fields.Nested(sets, skip_none=True), skip_none=True, description='list of sets of this exercise'),
        'pause': fields.Float(description='Pause before the next exercise starts')
    })

    workout = api.model('workout', {
        'id': fields.String(attribute='_id', description='workoutID'),
        'name': fields.String(description='name of the workout'),
        'user': fields.String(description='public_id of the user'),
        'notes': fields.String(description='notes'),
        'duration': fields.Float(description='duration of the workout'),
        'date': fields.DateTime(description='date of the workout'),
        'created': fields.DateTime(description='date of synchronisation'),
        'exercises': fields.List(fields.Nested(exercise, skip_none=True), skip_none=True, description='list of exercises of this workout')
    })