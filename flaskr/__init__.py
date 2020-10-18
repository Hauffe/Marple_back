import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    # WIN COMMANDS:
    # create and configure the app
    # $set FLASK_APP=flaskr
    # $set FLASK_ENV=development
    # $flask run
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.path.join('sqlite:///'+app.instance_path, 'marple.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    # ensure the instance folder exists
    try:
        os.makedirs('sqlite:///'+app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        from . import auth
        app.register_blueprint(auth.bp)

        db.create_all()

    return app
