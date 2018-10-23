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

from flask import abort, jsonify, make_response
from flask_restplus import Resource, fields, marshal
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound

from .app import api, app
from .models import Model, db


model_id = api.model('ModelID', {
    'id': fields.Integer
})


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
class ModelsResource(Resource):
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
        )).all()

    @api.expect(model)
    def post(self):
        """Create a new model."""
        app.logger.debug("Creating a new model in the model warehouse")
        new_model = Model(**api.payload)
        db.session.add(new_model)
        db.session.commit()
        # Return the created model resource identifier for convenience.
        resp = make_response(jsonify(marshal(new_model, model_id)), 201)
        # Return the relative URL to the new resource in the Location header.
        resp.headers["Location"] = f"/models/{new_model.id}"
        return resp


@api.response(404, 'Not found')
@api.route("/models/<int:id>",)
class ModelResource(Resource):
    """Retrieve, update or delete a single model."""

    @staticmethod
    def load_model(primary_id):
        """Load a model from the database by ID."""
        app.logger.debug("Loading model by ID %d.", primary_id)
        try:
            return Model.query.filter(Model.id == primary_id).one()
        except NoResultFound:
            abort(404, f"Cannot find any model with ID {primary_id}.")

    @api.marshal_with(model_full)
    def get(self, id):
        """Return a model by ID."""
        return self.load_model(id)

    @api.expect(model)
    @api.marshal_with(model_full)
    def put(self, id):
        """Update a model by ID."""
        model = self.load_model(id)
        app.logger.debug("Updating model.")
        model.__dict__.update(api.payload)
        db.session.commit()
        return "", 204

    @api.marshal_with(model_full)
    def delete(self, id):
        """Delete a model by ID."""
        model = self.load_model(id)
        app.logger.debug("Deleting model.")
        db.session.delete(model)
        db.session.commit()
        return "", 204
