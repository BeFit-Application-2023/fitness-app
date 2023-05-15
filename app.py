from flask import Flask, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session

from engineio.payload import Payload

from exercise_estimation.pose_estimator import PoseEstimation
from exercise_estimation.woker_supervisor import WorkerSupervisor

from blueprints.authentication import authentication_blueprint
from blueprints.home import home_page_blueprint
from blueprints.profile import profile_blueprint
from blueprints.trainer import trainer_blueprint
from blueprints.chatbot_api import chatbot_api_blueprint
from blueprints.telegram_auth import telegram_auth_blueprint

from models import *
from extension import *
from config import system_config

Payload.max_decode_packets = 2048

app = Flask(__name__)

app.register_blueprint(home_page_blueprint, url_prefix='/')
app.register_blueprint(authentication_blueprint, url_prefix='/')
app.register_blueprint(profile_blueprint, url_prefix='/')
app.register_blueprint(trainer_blueprint, url_prefix='/')
app.register_blueprint(telegram_auth_blueprint, url_prefix='/')
app.register_blueprint(chatbot_api_blueprint, url_prefix='/chatbot/')


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///detection.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Test2023-mysql-pl-claim!@localhost:3306/fitnessapp'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{system_config.MYSQL_USERNAME}:{system_config.MYSQL_PASSWORD}@{system_config.DATASTORE_URL}:{system_config.MYSQL_PORT}/{system_config.MYSQL_DBNAME}"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db.init_app(app)

Session(app)
socketio = SocketIO(app, cors_allowed_origins='*')

body_pose_estimator = PoseEstimation()
work_superviser = WorkerSupervisor()


@socketio.on('catch-frame')
def catch_frame(data):
    emit('response_back', data)


@socketio.on('connect')
def connect():
    work_superviser.add_worker(unique_sid=request.sid, data=Exercises, user_unique_id=session['user-id'])


@socketio.on('disconnect')
def disconnect():
    print('Disconnect', request.sid)


@socketio.on('image')
def image(data):
    user_sid = request.sid
    webp_image = data['image-webp']
    current_exercise = data['exercise']

    counter = work_superviser.run(sid=user_sid, frame=webp_image, exercise=current_exercise)

    emit('response_back', counter)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(app.url_map)

    socketio.run(app, port=8000, debug=True)
