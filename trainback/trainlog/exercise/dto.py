from flask_restx import fields
from trainback.trainlog.exercise import api


class ExerciseDto:
    name = api.model('name', {
        'de': fields.String(),
        'en': fields.String()
    })
    description = api.model('description', {
        'de': fields.String(),
        'en': fields.String()
    })

    exercise = api.model('exercise', {
        'id': fields.String(attribute='_id', description='exerciseID'),
        'name': fields.Nested(name, description='name of the exercise in diferent languages'),
        'description': fields.Nested(description, skip_none=True, description='description of the exercise in diferent languages'),
        'musclegroup': fields.List(fields.String, skip_none=True, description='list of musclegroups this exercise belongs to'),
        'machine': fields.Boolean(description='exercise need a machine or not')
    })