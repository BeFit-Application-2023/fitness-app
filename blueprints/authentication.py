from flask import Flask, Blueprint, request, render_template, redirect, session
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash

from models import *
from extension import db
from utils import *


authentication_blueprint = Blueprint('authentication_blueprint', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@authentication_blueprint.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        # if not (request.form.get('email') and request.form.get('password') \
        #     and request.form.get('first-name') and request.form.get('last-name')):
        #     return render_template('user_registration.html')

        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        context = {'message': 'Email already in use.'}

        if user:
            return redirect('/login')
        
        new_user = User(first_name=request.form.get('first-name'), second_name=request.form.get('last-name'), \
            email=request.form.get('email'), password=generate_password_hash(request.form.get('password')))

        db.session.add(new_user)
        db.session.commit()

        session['user-id'] = new_user.id

        return redirect('/physical-information')

    return render_template('user_registration.html')


@authentication_blueprint.route('/physical-information', methods=['POST', 'GET'])
def user_physical_information():
    if request.method == 'POST':

        user_imc = body_mass_index(height=float(request.form.get('height')), weight=float(request.form.get('weight')))
        datetime_object = datetime.strptime(request.form.get('birth-date'), '%Y-%m-%d')

        new_user = UserPhysicalInformation(user_id=session['user-id'], birthday=datetime_object, \
            weight=request.form.get('weight'), height=request.form.get('height'), bmi=user_imc, \
            goal=request.form.get('goals'), level=request.form.get('level'))

        db.session.add(new_user)
        db.session.commit()

        session['user-id'] = new_user.id

        return redirect('/profile')

    return render_template('user_physical_information.html')


@authentication_blueprint.route('/login', methods=['POST', 'GET'])
def login_post():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return render_template('user_registration.html') # if the user doesn't exist or password is wrong, reload the page
        session['user-id'] = user.id
        # if the above check passes, then we know the user has the right credentials
        return redirect('/profile')

    return render_template('login.html')