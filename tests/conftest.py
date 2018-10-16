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

"""Provide session level fixtures."""

import pytest
from jose import jwt

from model_storage.app import api
from model_storage.app import app as app_
from model_storage.app import init_app
from model_storage.models import Model
from model_storage.models import db as db_


@pytest.fixture(scope="session")
def app():
    """Provide an initialized Flask for use in certain test cases."""
    init_app(app_, api, db_)
    with app_.app_context():
        yield app_


@pytest.fixture(scope="session")
def client(app):
    """Provide a Flask test client to be used by almost all test cases."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def db(app):
    """Provide a database session with tables created."""
    db_.create_all()
    yield db_
    db_.session.remove()
    db_.drop_all()


@pytest.fixture(scope='function')
def models(db):
    """Return a fixture with test data for the Model data model."""
    fixture1 = Model(
        id=1,
        name="Restricted Model",
        organism_id="4",
        project_id=4,
        default_biomass_reaction="BIOMASS",
        model_serialized={"Reactions": [{"GAPDH": "x->y"}]},
    )
    fixture2 = Model(
        id=2,
        name="Public Model",
        organism_id="5",
        project_id=None,
        default_biomass_reaction="BIOMASS",
        model_serialized={"Reactions": [{"GAPDH": "x->y"}]},
    )
    db.session.add(fixture1)
    db.session.add(fixture2)
    return fixture1, fixture2


@pytest.fixture(scope="session")
def tokens(app):
    """Provides read, write and admin JWT claims to project 4"""
    return {
        'read': jwt.encode(
            {'prj': {4: 'read'}},
            app.config['JWT_PRIVATE_KEY'],
            'RS512',
        ),
        'write': jwt.encode(
            {'prj': {4: 'write'}},
            app.config['JWT_PRIVATE_KEY'],
            'RS512',
        ),
        'admin': jwt.encode(
            {'prj': {4: 'admin'}},
            app.config['JWT_PRIVATE_KEY'],
            'RS512',
        ),
    }
