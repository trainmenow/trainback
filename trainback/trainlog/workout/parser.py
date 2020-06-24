from flask_restx import reqparse, inputs
from datetime import datetime
from cerberus import Validator
import json


def workout_validator(value):
    if isinstance(value, str):
        value = json.loads(value)
    value['date'] = datetime.strptime(value['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    SCHEMA = {
        'name': {'type': 'string', 'required': True},
        'user': {'type': 'string', 'required': False},
        'notes': {'type': 'string', 'required': False},
        'duration': {'type': 'number', 'required': True},
        'date': {'type': 'datetime', 'required': True},
        'created': {'type': 'datetime', 'required': False, 'default': datetime.utcnow()},
        'exercises': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'sets': {
                        'type': 'list',
                        'required': True,
                        'schema': {
                            'type': 'dict',
                            'required': True,
                            'schema': {
                                'kind': {'type': 'string', 'required': False, 'default': 'normale'},
                                'repeats': {'type': 'integer', 'required': False},
                                'weight': {'type': 'number', 'required': False},
                                'distance': {'type': 'number', 'required': False},
                                'time': {'type': 'number', 'required': False, 'default': 0},
                                'pause': {'type': 'number', 'required': False, 'default': 0}
                            }
                        }
                    },
                    'exercise': {'type': 'string', 'required': True },
                    'pause': {'type': 'number', 'required': False, 'default': 0}
                }
            }
        }
    }
    
    v = Validator(SCHEMA)
    v.allow_unknown = False
    if v.validate(value):
        return v.document
    else:
        raise ValueError(json.dumps(v.errors))


workout_parser = reqparse.RequestParser()
workout_parser.add_argument('workout', type=workout_validator, required=True, help='Example: {"name": "name", "duration": 43, "date": "2012-05-29T19:30:03.283Z", "exercises": [{"sets": [{ "kind": "warm-up", "repeats": 15, "weight": 45.3 }], "exercise": "3785837tergn4398" }]} Error:')