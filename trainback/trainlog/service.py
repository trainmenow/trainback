from trainback import mongo

def get_exercises():
    return list(mongo.db.exercises.find())