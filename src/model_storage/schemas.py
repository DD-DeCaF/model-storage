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

from marshmallow import Schema, fields


class Model(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    organism_id = fields.Integer(required=True)
    project_id = fields.Integer(required=True)
    model_serialized = fields.Raw(
        description="A metabolic model serialized to JSON by cobrapy",
        required=True,
    )
    default_biomass_reaction = fields.String(required=True)
    preferred_map_id = fields.Integer(required=True)

    class Meta:
        strict = True
