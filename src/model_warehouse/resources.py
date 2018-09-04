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

from flask_restplus import Resource, fields

from .app import api, app
from .models import Model, db


# TODO: Impelment schema inheritance
input_model_schema = api.model('NewModel', {
    'name': fields.String,
    'model_serialized': fields.Raw(
        title='Metabolic Model JSON',
        description='A metabolic model serialized to JSON by cobrapy',
        required=True, readonly=False
    ),
    'organism_id': fields.String,
    'project_id': fields.Integer,
    'default_biomass_reaction': fields.String,
})


model_schema = api.model('Model', {
    'created': fields.DateTime,
    'updated': fields.DateTime,
    'id': fields.Integer,
    'name': fields.String,
    'model_serialized': fields.Raw(
        title='Metabolic Model JSON',
        description='A metabolic model serialized to JSON by cobrapy',
        required=True, readonly=False
    ),
    'organism_id': fields.String,
    'project_id': fields.Integer,
    'default_biomass_reaction': fields.String,
})


@api.response(404, 'Not found')
@api.route("/models")
class Models(Resource):
    """Serve all available models or create new entries."""

    @api.marshal_with(model_schema)
    def get(self):
        """List all available models."""
        app.logger.debug("Retrieving all models")
        return Model.query.all()


    @api.expect(input_model_schema)
    @api.marshal_with(model_schema)
    def post(self):
        """Create a new model."""
        app.logger.debug("Creating a new model in the model warehouse")
        new_model = Model(**api.payload)
        db.session.add(new_model)
        db.session.commit()
        return new_model


@api.response(404, 'Not found')
@api.route("/models/<int:id>",)
class IndvModel(Resource):
    """Retrieve, update or delete a single model."""

    @api.marshal_with(model_schema)
    def get(self, id):
        """Return a model by ID."""
        app.logger.debug("Fetching model by ID {}".format(id))
        return Model.query.filter(Model.id == id).one()

    @api.expect(input_model_schema)
    @api.marshal_with(model_schema)
    def put(self, id):
        """Update a model by ID."""
        app.logger.debug("Updating model by ID {}".format(id))
        model = Model.query.filter(Model.id == id).one()
        for key, value in api.payload.items():
            setattr(model, key, value)
        db.session.commit()
        return model

    @api.marshal_with(model_schema)
    def delete(self, id):
        """Delete a model by ID."""
        app.logger.debug("Deleting model by ID {}".format(id))
        model = Model.query.filter(Model.id == id).one()
        db.session.delete(model)
        db.session.commit()
        return model
