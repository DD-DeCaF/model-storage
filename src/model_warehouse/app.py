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

"""Expose the main Flask-RESTPlus application."""

import logging
import logging.config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restplus import Api
from raven.contrib.flask import Sentry

from werkzeug.contrib.fixers import ProxyFix
from model_warehouse.settings import current_config


app = Flask(__name__)
app.config.from_object(current_config())
api = Api(
    title="model_warehouse",
    version="0.1.0",
    description="The storage for metabolic models used by the platform",
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def init_app(application, interface):
    """Initialize the main app with config information and routes."""
    application.config.from_object(current_config())

    # Configure logging
    logging.config.dictConfig(application.config['LOGGING'])

    # Configure Sentry
    if application.config['SENTRY_DSN']:
        sentry = Sentry(dsn=application.config['SENTRY_DSN'], logging=True,
                        level=logging.ERROR)
        sentry.init_app(application)

    # Add routes and resources.
    from model_warehouse import resources
    interface.init_app(application)

    # Add CORS information for all resources.
    CORS(application)

    # Please keep in mind that it is a security issue to use such a middleware
    # in a non-proxy setup because it will blindly trust the incoming headers
    # which might be forged by malicious clients.
    # We require this in order to serve the HTML version of the OpenAPI docs
    # via https.
    application.wsgi_app = ProxyFix(application.wsgi_app)
