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

"""Implement RESTful API endpoints using resources."""

import logging

from flask import abort, g, make_response
from flask_apispec import FlaskApiSpec, MethodResource, marshal_with, use_kwargs
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound

from .jwt import jwt_require_claim, jwt_required
from .models import Model, db
from .schemas import Model as ModelSchema


logger = logging.getLogger(__name__)


def init_app(app):
    """Register API resources on the provided Flask application."""
    def register(path, resource):
        app.add_url_rule(path, view_func=resource.as_view(resource.__name__))
        docs.register(resource, endpoint=resource.__name__)

    docs = FlaskApiSpec(app)
    register("/models", Models)
    register("/models/<int:id>", IndvModel)


class Models(MethodResource):
    """Serve all available models or create new entries."""

    @marshal_with(ModelSchema(many=True, exclude=('model_serialized',)))
    def get(self):
        """List all available models."""
        logger.debug("Retrieving all models")
        return Model.query.options(load_only(
            Model.id,
            Model.name,
            Model.organism_id,
            Model.project_id,
            Model.preferred_map_id,
            Model.default_biomass_reaction,
            Model.ec_model,
        )).filter(
            Model.project_id.in_(g.jwt_claims['prj']) |
            Model.project_id.is_(None)
        ).all()

    @use_kwargs(ModelSchema(exclude=('id',)))
    @marshal_with(ModelSchema(only=('id',)), code=201)
    @jwt_required
    def post(self, **payload):
        """Create a new model."""
        logger.debug("Creating a new model in the model storage")
        if 'project_id' in payload:
            jwt_require_claim(payload['project_id'], 'write')
        new_model = Model(**payload)
        db.session.add(new_model)
        db.session.commit()
        return new_model, 201


class IndvModel(MethodResource):
    """Retrieve, update or delete a single model."""

    @marshal_with(ModelSchema, code=200)
    @marshal_with(None, code=404)
    def get(self, id):
        """Return a model by ID."""
        logger.debug(f"Fetching model by ID {id}.")
        try:
            return Model.query.filter(
                Model.id == id
            ).filter(
                Model.project_id.in_(g.jwt_claims['prj']) |
                Model.project_id.is_(None)
            ).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with ID {id}.")

    @use_kwargs(ModelSchema(exclude=('id',), partial=True))
    @marshal_with(None, code=204)
    @marshal_with(None, code=404)
    @jwt_required
    def put(self, id, **payload):
        """Update a model by ID."""
        logger.debug(f"Updating model with ID {id}.")
        try:
            model = Model.query.filter(Model.id == id).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with ID {id}.")
        jwt_require_claim(model.project_id, 'write')
        for key, value in payload.items():
            setattr(model, key, value)
        db.session.commit()
        return make_response("", 204)

    @marshal_with(None, code=204)
    @marshal_with(None, code=404)
    @jwt_required
    def delete(self, id):
        """Delete a model by ID."""
        logger.debug(f"Deleting model with ID {id}.")
        try:
            model = Model.query.filter(Model.id == id).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with ID {id}.")
        jwt_require_claim(model.project_id, 'admin')
        db.session.delete(model)
        db.session.commit()
        return make_response("", 204)
