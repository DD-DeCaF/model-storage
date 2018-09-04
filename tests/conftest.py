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

from model_warehouse.app import api
from model_warehouse.app import app as app_
from model_warehouse.app import init_app
from model_warehouse.models import Model
from model_warehouse.models import db as db_


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
def model(db):
    """Return a fixture with test data for the Model data model."""
    fixture = Model(name="iJO1366", organism_id="4",
                  project_id=4, default_biomass_reaction="BIOMASS",
                  model_serialized={"Reactions":[{"GAPDH":"x->y"}]}
    )
    db.session.add(fixture)
    return fixture
