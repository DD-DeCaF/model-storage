# Copyright 2018 Novo Nordisk Foundation Center for Biosustainability, DTU.
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
# limitations under the License.from datetime import datetime


from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql


db = SQLAlchemy()


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Model(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    model_serialized = db.Column(postgresql.JSONB, nullable=False)
    organism_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer)
    default_biomass_reaction = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        """Return a printable representation."""
        return f"<{self.__class__.__name__} {self.id}: {self.name}>"
