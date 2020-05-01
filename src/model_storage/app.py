# Copyright (c) 2018, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Expose the main Flask application."""

import json
import logging
import logging.config

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from raven.contrib.flask import Sentry
from werkzeug.middleware.proxy_fix import ProxyFix

from . import errorhandlers, jwt, resources
from .models import Model
from .settings import current_config


app = Flask(__name__)
app.config.from_object(current_config())


def init_app(application, db):
    """Initialize the main app with config information and routes."""
    application.config.from_object(current_config())

    # Configure logging
    logging.config.dictConfig(application.config["LOGGING"])
    db.init_app(application)
    Migrate(application, db)

    # Configure Sentry
    if application.config["SENTRY_DSN"]:
        sentry = Sentry(
            dsn=application.config["SENTRY_DSN"],
            logging=True,
            level=logging.ERROR,
        )
        sentry.init_app(application)

    # Add routes and resources.
    resources.init_app(application)

    # Add CORS information for all resources.
    CORS(application)

    # Add JWT middleware
    jwt.init_app(application)

    # Register error handlers
    errorhandlers.init_app(application)

    # Please keep in mind that it is a security issue to use such a middleware
    # in a non-proxy setup because it will blindly trust the incoming headers
    # which might be forged by malicious clients.
    # We require this in order to serve the HTML version of the OpenAPI docs
    # via https.
    application.wsgi_app = ProxyFix(application.wsgi_app)

    # Add Flask CLI command to install fixtures in the database
    app.logger.debug("Registering CLI commands")

    @application.cli.command()
    def make_fixtures():
        with open("fixtures/models.json") as json_data:
            fixtures = json.load(json_data)
        for fixture in fixtures["rest-api-fixtures"]:
            model = Model(**fixture)
            db.session.add(model)
        db.session.commit()

    app.logger.info("App initialization complete")
