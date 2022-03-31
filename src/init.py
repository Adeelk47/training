import logging
from typing import NoReturn

from flask import current_app as app
from flask_cors import CORS
from flask_migrate import Migrate

from api import blueprint
from conf import settings
from model.base import db


def initialize_app() -> NoReturn:
    """
    Set app configs

    :return:
    """

    logging.getLogger().setLevel(level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CORS_HEADERS"] = "Content-Type"

    app.register_blueprint(blueprint, url_prefix="/api/v1")
    db.init_app(app)
    Migrate(app, db)

    CORS(app, max_age=600)
