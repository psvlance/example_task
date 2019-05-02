from typing import Callable

from flask import Flask
from werkzeug.debug import DebuggedApplication


def _app_singleton():
    app = None

    def _create_app_fabric(settings: Callable = None, extensions: iter = None) -> Callable:
        nonlocal app

        if app:
            return app

        app = Flask(__name__)

        if settings:
            app.config.from_object(settings)

        if extensions:
            for Extension in extensions:
                obj = Extension(app)

        if app.debug:
            app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

        return app
    return _create_app_fabric


def _marshmallow_singleton():
    ma = None

    def _create_marshmallow_fabric():
        nonlocal ma
        if ma:
            return ma

        from flask_marshmallow import Marshmallow
        app = create_app_fabric()
        ma = Marshmallow(app)
        return ma

    return _create_marshmallow_fabric


def _database_singleton():
    db = None

    def _create_database_fabric():
        nonlocal db
        if db:
            return db

        from flask_sqlalchemy import SQLAlchemy
        app = create_app_fabric()
        if not app.config.get('SQLALCHEMY_DATABASE_URI', None):
            app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
        db = SQLAlchemy(app)
        return db

    return _create_database_fabric


def register_bps(*args):
    app = create_app_fabric()

    from api.api import api
    app.register_blueprint(api)


create_app_fabric = _app_singleton()
create_marshmallow_fabric = _marshmallow_singleton()
create_database_fabric = _database_singleton()
