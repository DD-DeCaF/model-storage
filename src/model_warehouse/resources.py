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

from model_warehouse.app import api, app

# TODO: Impelment schema inheritance
input_model_schema = api.model('NewModel', {
    'name': fields.String,
    'model_serialized': fields.Raw(
        title='Metabolic Model JSON',
        description='A metabolic model serialized to JSON by cobrapy',
        required=True, readonly=False
    ),
    'organism_id': fields.Integer,
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
    'organism_id': fields.Integer,
    'project_id': fields.Integer,
    'default_biomass_reaction': fields.String,
})


def post(obj, *args, **kwargs):
    """Determine if the payload is a single model or multiple models."""
    if isinstance(api.payload, dict):
        return obj.post_one(api.payload, *args, **kwargs)
    elif isinstance(api.payload, list):
        return [obj.post_one(data, *args, **kwargs) for data in api.payload]
    else:
        raise ValueError(f"Unsupported API payload type '{type(api.payload)}'")


@api.response(404, 'Not found')
@api.route("/models")
class Models(Resource):
    """Serve all available models or create new entries."""

    def get(self):
        """List all available models"""
        app.logger.debug("Getting stuff!")
        return "Getting all models for ya"

    @api.expect(input_model_schema)
    @api.marshal_with(input_model_schema)
    def post(self):
        """Create a new model (accepts an object or an array of objects)"""
        app.logger.debug("Getting stuff!")
        return post(self)

    def post_one(self, data):
        """Create a single model"""
        return data


@api.response(404, 'Not found')
@api.route("/models/<int:id>",)
class Model(Resource):
    """Retrieve, update or delete a single model."""

    def get(self, id):
        """Return a model by ID."""
        app.logger.debug("Getting stuff!")
        return "Displaying Model IDs".format(id)

    @api.marshal_with(model_schema)
    @api.expect(model_schema)
    def put(self, id):
        """Update a model by ID."""
        app.logger.debug("Getting stuff!")
        return "Displaying Model IDs".format(id)

    def delete(self, id):
        """Delete a model by ID."""
        app.logger.debug("Getting stuff!")
        return "Displaying Model IDs".format(id)

