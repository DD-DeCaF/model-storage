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

from cobra.io.dict import model_from_dict
from marshmallow import Schema, ValidationError, fields, validates_schema


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
    preferred_map_id = fields.Integer(allow_none=True)

    @validates_schema
    def validate_biomass(self, data):
        if 'model_serialized' in data:
            # Validate that the model can be loaded by cobrapy
            try:
                model = model_from_dict(data['model_serialized'])
            except Exception as error:
                raise ValidationError(str(error))

            # Validate that given biomass reaction exists in the model
            if 'default_biomass_reaction' in data:
                if data['default_biomass_reaction'] not in model.reactions:
                    raise ValidationError(
                        f"The biomass reaction "
                        f"'{data['default_biomass_reaction']}' does not exist "
                        f"in the corresponding model."
                    )

    class Meta:
        strict = True
