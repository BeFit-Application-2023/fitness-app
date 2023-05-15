from datetime import datetime

from flask import Blueprint, request, render_template, session

from models import *
from extension import db
from utils import *


profile_blueprint = Blueprint('profile_blueprint', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@profile_blueprint.route('/profile', methods=['POST', 'GET'])
def profile():
    print(session['user-id'])
    user = User.query.filter_by(id=session['user-id']).first()

    new_exercise = Exercises(
        user_id=session['user-id'], 
        for_datetime=datetime.now(),
        exercise_1='squats', count_1=30, 
        exercise_2='push-ups', count_2=30, 
        exercise_3='bridge', count_3=30 
        # exercise_4='stand-alone', count_4=30, 
        )
    
    db.session.add(new_exercise)
    db.session.commit()

    user_exercises = Exercises.query.filter_by(user_id=session['user-id']).all()[-1]

    context = {
        'first_name': user.first_name,
        'second_name': user.second_name,
        'email': user.email,
        'exercise_list': [user_exercises.exercise_1, user_exercises.exercise_2, user_exercises.exercise_3],
        'exercise_count': [user_exercises.count_1, user_exercises.count_2, user_exercises.count_3],
        'exercise_id': [1, 2, 3],
        }
    
    return render_template('profile.html', **context)
