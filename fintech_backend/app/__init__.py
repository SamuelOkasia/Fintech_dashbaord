from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import os


def create_app():
    app = Flask(__name__)
    CORS(app)

    UPLOAD_FOLDER = 'app/upload_folder'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.blueprints.dashboard.routes import dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from app.blueprints.populate.routes import populate_blueprint
    app.register_blueprint(populate_blueprint)

    from app.blueprints.page.routes import page_blueprint
    app.register_blueprint(page_blueprint)


    return app
