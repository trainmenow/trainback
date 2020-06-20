from flask_restx import reqparse, inputs


exercise_parser = reqparse.RequestParser()
exercise_parser.add_argument('name', type=dict, required=True, help='name of the exercise in different languages')
exercise_parser.add_argument('description', type=dict, required=True, help='description of the exercise in different languages')
exercise_parser.add_argument('musclegroup', type=list, required=True, help='list of musclegroups this exercise belongs to')
exercise_parser.add_argument('machine', type=inputs.boolean, required=True, help='exercise need a machine or not')