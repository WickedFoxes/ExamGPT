from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os
import config

db = SQLAlchemy()
migrate = Migrate()
UPLOAD_FOLDER = 'ept/static/uploads'
ALLOWED_EXTENSIONS = {
    'text/plain', 'text/html', 'application/pdf', 'image/png', 'image/jpeg',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', # pptx
    'application/vnd.ms-powerpoint', # ppt
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' # docx
    'application/msword', #doc
}
TOKEN_LIMIT = 1200

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TOKEN_LIMIT'] = TOKEN_LIMIT

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트
    from .views import main_views, question_views, auth_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app