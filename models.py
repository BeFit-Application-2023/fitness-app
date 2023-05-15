from extension import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    first_name = db.Column(db.String(64), nullable=False) 
    second_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  

    def __init__(self, first_name, second_name, email, password):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = password


class UserPhysicalInformation(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), nullable=False) 
    birthday = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float(), nullable=False)
    height = db.Column(db.Float(), nullable=False)  
    bmi = db.Column(db.Float(), nullable=False)
    goal = db.Column(db.String(32), nullable=False)
    level = db.Column(db.String(32), nullable=False)

    def __init__(self, user_id, birthday, weight, height, bmi, goal, level):
        self.user_id = user_id
        self.birthday = birthday
        self.weight = weight
        self.height = height
        self.bmi = bmi
        self.goal = goal
        self.level = level


class Goals(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), nullable=False) 
    goal_type = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(64), nullable=False)  

    def __init__(self, user_id, goal_type, value, status):
        self.user_id = user_id
        self.goal_type = goal_type
        self.value = value
        self.status = status


class Exercises(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), nullable=False) 
    datetime = db.Column(db.DateTime, nullable=False)
    exercise_1 = db.Column(db.String(64), nullable=False)
    count_1 = db.Column(db.Integer(), nullable=False)
    exercise_2 = db.Column(db.String(64), nullable=False)
    count_2 = db.Column(db.Integer(), nullable=False)
    exercise_3 = db.Column(db.String(64), nullable=False)
    count_3 = db.Column(db.Integer(), nullable=False)

    def __init__(self, user_id, for_datetime, exercise_1, exercise_2, exercise_3, count_1, count_2, count_3):
        self.user_id = user_id
        self.datetime = for_datetime
        self.exercise_1 = exercise_1
        self.exercise_2 = exercise_2
        self.exercise_3 = exercise_3
        self.count_1 = count_1
        self.count_2 = count_2
        self.count_3 = count_3


class TelegramAuthTokens(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), nullable=False) 
    auth_token = db.Column(db.String(16), nullable=False)
    
    def __init__(self, user_id, auth_token):
        self.user_id = user_id
        self.auth_token = auth_token
