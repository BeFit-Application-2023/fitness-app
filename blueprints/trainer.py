from flask import Flask, Blueprint, request, render_template, redirect, session
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash

from models import *
from extension import db
from utils import *


trainer_blueprint = Blueprint('trainer_blueprint', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@trainer_blueprint.route('/training-session', methods=['POST', 'GET']) 
def trainer():
    user_exercises = Exercises.query.filter_by(user_id=session['user-id']).all()[-1]
    user = User.query.filter_by(id=session['user-id']).first()

    context = {
        'exercise_list': [user_exercises.exercise_1, user_exercises.exercise_2, user_exercises.exercise_3],
        'exercise_count': [user_exercises.count_1, user_exercises.count_2, user_exercises.count_3],
        'exercise_id': [1, 2, 3],
        'first_name': user.first_name,
        'second_name': user.second_name,
        # 'email': user.email
        }
    
    return render_template('stream.html', **context)