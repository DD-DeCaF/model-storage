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

from flask import abort, g
from flask_restplus import Resource, fields
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound

from .app import api, app
from .jwt import jwt_require_claim, jwt_required
from .models import Model, db


model_header = api.model('ModelHeader', {
    'id': fields.Integer,
    'name': fields.String,
    'organism_id': fields.String,
    'project_id': fields.Integer,
})


model = api.inherit('Model', model_header, {
    'model_serialized': fields.Raw(
        title='Metabolic Model JSON',
        description='A metabolic model serialized to JSON by cobrapy',
        required=True, readonly=False
    ),
    'organism_id': fields.String,
    'project_id': fields.Integer,
    'default_biomass_reaction': fields.String,
})


model_full = api.inherit('ModelFull', model, {
    'created': fields.DateTime,
    'updated': fields.DateTime,
})


@api.route("/models")
class Models(Resource):
    """Serve all available models or create new entries."""

    @api.marshal_with(model_header)
    def get(self):
        """List all available models."""
        app.logger.debug("Retrieving all models")
        return Model.query.options(load_only(
            Model.id,
            Model.name,
            Model.organism_id,
            Model.project_id,
        )).filter(
            Model.project_id.in_(g.jwt_claims['prj'])
            | Model.project_id.is_(None)
        ).all()

    @api.expect(model)
    @api.marshal_with(model_full)
    @jwt_required
    def post(self):
        """Create a new model."""
        app.logger.debug("Creating a new model in the model storage")
        if 'project_id' in api.payload:
            jwt_require_claim(api.payload['project_id'], 'write')
        new_model = Model(**api.payload)
        db.session.add(new_model)
        db.session.commit()
        return new_model


@api.response(404, 'Not found')
@api.route("/models/<int:id>",)
class IndvModel(Resource):
    """Retrieve, update or delete a single model."""

    @api.marshal_with(model_full)
    def get(self, id):
        """Return a model by ID."""
        app.logger.debug("Fetching model by ID {}".format(id))
        try:
            return Model.query.filter(
                Model.id == id
            ).filter(
                Model.project_id.in_(g.jwt_claims['prj'])
                | Model.project_id.is_(None)
            ).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with id {id}")

    @api.expect(model)
    @api.marshal_with(model_full)
    @jwt_required
    def put(self, id):
        """Update a model by ID."""
        app.logger.debug("Updating model by ID {}".format(id))
        try:
            model = Model.query.filter(Model.id == id).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with id {id}")
        jwt_require_claim(model.project_id, 'write')
        for key, value in api.payload.items():
            setattr(model, key, value)
        db.session.commit()
        return model

    @api.marshal_with(model_full)
    @jwt_required
    def delete(self, id):
        """Delete a model by ID."""
        app.logger.debug("Deleting model by ID {}".format(id))
        try:
            model = Model.query.filter(Model.id == id).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with id {id}")
        jwt_require_claim(model.project_id, 'admin')
        db.session.delete(model)
        db.session.commit()
        return model
