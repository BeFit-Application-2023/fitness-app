import random

from flask import Blueprint, request, render_template, session

from models import *
from extension import db
from utils import *


telegram_auth_blueprint = Blueprint('telegram-sync', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@telegram_auth_blueprint.route('/telegram-sync', methods=['POST', 'GET'])
def telegram():
    user = TelegramAuthTokens.query.filter_by(user_id=session['user-id']).first()

    auth_token = user.auth_token if user is not None else None

    if not auth_token:

        auth_token = 'TG' + '-' + str(random.randint(10000, 99999))
        new_auth_token = TelegramAuthTokens(user_id=session['user-id'], auth_token=auth_token)

        db.session.add(new_auth_token)
        db.session.commit()

    context = {
        'telegram_auth_token': auth_token
    }

    return render_template('telegram_auth.html', **context)

