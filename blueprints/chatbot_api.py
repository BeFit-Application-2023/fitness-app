from flask import Blueprint, request, render_template, session, jsonify

from models import *
from extension import db
from utils import *


chatbot_api_blueprint = Blueprint('chatbot', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


# # Get progress
# # no payload

# # Response structure
# get_progress_no_progress = {
#     "exists" : "no-progress"
# }

# get_progress = {
#     "exists" : "exists",
#     "value" : 90,
#     "measure_of_progress" : "kgs"
# }

# # Get kcals burned
# # Payload.
# {
#     "date" : "%Y-%m-%d"
# }
# # Response.
# kcals_burned = {
#     "date" : "2023-01-10",
#     "kcals_burned" : 100
# }



@chatbot_api_blueprint.route('/get-id', methods=['POST', 'GET'])
def get_id():

    """
    Request template
        {
            "code": <code>
        }
    """
    try:
        authentication_info = TelegramAuthTokens.query.filter_by(auth_token=request.form.get('code')).first()

        return {'user-id': authentication_info.auth_token}, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301


@chatbot_api_blueprint.route('/get-exercise', methods=['POST', 'GET'])
def get_exercises():

    """
        {
            "user-id": <user_id>,
            "datetime": <datetime>
        }
    """

    try:
        exercise_user_data = Exercises.query.filter_by(user_id = request.form.get('user-id'), datetime=request.form.get('datetime')).first()
        exercise_info = {
            "date" : request.form.get('datetime'),
            "user-id": request.form.get('user-id'),
            "exercises" : [
                {
                    "type" : exercise_user_data.exercise_1, "count" : exercise_user_data.count_1,
                },
                {
                    "type" : exercise_user_data.exercise_2, "count" : exercise_user_data.count_2,
                },
                {
                    "type" : exercise_user_data.exercise_3, "count" : exercise_user_data.count_3,
                }
            ]
        }
        return exercise_info, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301


@chatbot_api_blueprint.route('/get-meal', methods=['POST', 'GET'])
def get_meal():
    """
        {
            Prosta request
        }
    """
    try:
        get_meals = {
            "date" : "2023-01-10",
            "meals" : {
                "breakfast" : {"omlet" : 200},
                "lunch" : {"bors" : 300},
                "dinner" : {"cesar salad" : 100}
            }
        }
        return get_meals, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301


@chatbot_api_blueprint.route('/get-kcal-gained', methods=['POST', 'GET'])
def get_kcal_gained():
    """
        {
            Prosta request
        }
    """
    try:
        kcals_gained = {
            "date" : "2023-01-10",
            "kcals_gained" : 100
        }
        return kcals_gained, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301


@chatbot_api_blueprint.route('/get-stats', methods=['POST', 'GET'])
def get_physical_information():
    """
        {
            "user-id": <user_id>
        }
    """
    try:
        user_physical_info = UserPhysicalInformation.query.filter_by(user_id=request.form.get('user-id'))
        get_stats = {
            "weight" : user_physical_info.weight,
            "height" : user_physical_info.height
        }
        return get_stats, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301


@chatbot_api_blueprint.route('/update-stats', methods=['POST', 'GET'])
def update_stats():

    """
        {
            "user-id": <user_id>,
            "height": <height>,
            "weight": <weight>
        }
    """

    try:
        user_physical_information = UserPhysicalInformation.query.filter_by(user_id=request.form.get('user-id')).first()
        user_physical_information.weight = request.form.get('weight')
        user_physical_information.height = request.form.get('height')
        user_physical_information.bmi = body_mass_index(height=request.form.get('height'), weight=request.form.get('weight'))
        
        db.session.commit()

        return {'result': 'Physical information successfully updated!'}, 200
    except:
        pass
    return {'message': 'Bad request.'}, 301