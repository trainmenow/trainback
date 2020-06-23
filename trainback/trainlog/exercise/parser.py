from flask_restx import reqparse, inputs
from cerberus import Validator
import json


def exercise_validator(value):
    if isinstance(value, str):
        value = json.loads(value)

    SCHEMA = {
        'name': {
            'type': 'dict',
            'required': True,
            'schema': {
                'de': {'required': True, 'type': 'string'},
                'en': {'required': False, 'type': 'string'}
            }
        },
        'description': {
            'type': 'dict',
            'required': True,
            'schema': {
                'de': {'required': True, 'type': 'string'},
                'en': {'required': False, 'type': 'string'}
            }
        },
        'musclegroup': {
            'type': 'list',
            'required': True,
            'schema': {'type': 'string'}
        },
        'machine': {
            'type': 'boolean',
            'required': True
        }
    }

    v = Validator(SCHEMA)
    v.allow_unknown = False
    if v.validate(value):
        return v.document
    else:
        raise ValueError(json.dumps(v.errors))


exercise_parser = reqparse.RequestParser()
exercise_parser.add_argument('exercise', type=exercise_validator, required=True, help='Example: { "name": { "de": "Name", "en": "name" }, "description": { "de": "Beschreibung", "en": "description" },	"musclegroup": ["chest", "arms"], "machine": false } Error: ')