import logging
import sys
from flask import Flask
from pullsbury.db import init_app


def create_app(config):
    app = Flask("pullsbury")
    app.config.update(config)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
    init_app(app)

    return app
