from flask import Blueprint, request, render_template, redirect


home_page_blueprint = Blueprint('home_page_blueprint', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@home_page_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/registration')
    return render_template('home.html')
