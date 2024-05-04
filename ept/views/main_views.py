from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('question._list'))

@bp.route('/error')
def error():
    return render_template('error.html')

@bp.route('/exam_create_error')
def exam_create_error():
    return render_template('exam_create_error.html')