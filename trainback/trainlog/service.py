from trainback import mongo

def get_exercises():
    return list(mongo.db.exercises.find()), 200

def create_exercise(data):
    exercise_id = mongo.db.exercises.insert_one(data).inserted_id
    return str(exercise_id), 201

def create_workout(data, public_id):
    data['user'] = public_id
    workout_id = mongo.db.workouts.insert_one(data).inserted_id
    return str(workout_id), 201

def get_workouts_by_user(public_id):
    workouts = list(mongo.db.workouts.find({"user": public_id}, sort=[('date', -1)]))       
    return workouts, 200

def get_workout_by_id(id, public_id):
    workout = mongo.db.workouts.find_one_or_404({"_id": id, "user": public_id})
    return workout, 200

def del_workout_by_id(id, public_id):
    workout = mongo.db.workouts.find_one_or_404({"_id": id, "user": public_id})
    mongo.db.workouts.delete_one("workout")
    return {'error': False, 'message': 'Workout has been deleted'}, 205

def replace_workout(id, public_id, data):
    workout = mongo.db.workouts.find_one_or_404({"_id": id, "user": public_id})
    data['user'] = public_id
    workout = mongo.db.workouts.replace_one(workout, data)
    return {'error': False, 'message': 'Workout has been updated'}, 202