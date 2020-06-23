from trainback import mongo

def get_exercises():
    return list(mongo.db.exercises.find())

def create_exercise(data):
    exercise_id = mongo.db.exercises.insert_one(data).inserted_id
    return str(exercise_id), 201

def create_workout(data, pub_id):
    data['user'] = pub_id
    workout_id = mongo.db.workouts.insert_one(data).inserted_id
    return str(workout_id), 201