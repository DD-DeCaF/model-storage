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

"""Test expected functioning of the OpenAPI docs endpoints."""


def test_models_get(client, db, models):
    """Test the /models GET API supposed to return all models in the DB."""
    db.session.commit()
    resp = client.get("/models")
    assert resp.status_code == 200
    assert len(resp.json) == 1


def test_models_post(client, db, tokens):
    """Test the /models POST API supposed to post a single model to the DB."""
    new_model = {
        "name": "iML12311",
        "model_serialized": {"Something Here": "And Here"},
        "organism_id": "This is a String! 0123456789",
        "project_id": 4,
        "default_biomass_reaction": "BIOMASS"
    }

    resp = client.post("/models", json=new_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == 200


def test_indvmodel_get(client, db, models, tokens):
    """Test the /models/<id> GET API supposed to get a single model by ID."""
    db.session.commit()
    resp = client.get("/models/1", headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert resp.status_code == 200


def test_indvmodel_put(client, db, models, tokens):
    """Test the /models/<id> PUT API supposed to modify a single model by ID."""
    db.session.commit()
    updated_model = {
        "name": "iJO1366",
        "model_serialized": {"Reactions": [{"GAPDH": "x->y"},
                                           {"PMMO": "a->z"}]},
        "organism_id": "EColi",
        "project_id": 1,
        "default_biomass_reaction": "BIOMASS_RXN_ecoli"
    }
    resp = client.put("/models/1", json=updated_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == 200


def test_indvmodel_delete(client, db, models, tokens):
    """Test the /models/<id> PUT API supposed to remove a single model by ID."""
    db.session.commit()
    resp = client.delete("/models/1", headers={
        'Authorization': f"Bearer {tokens['admin']}",
    })
    assert resp.status_code == 200


def test_indvmodel_not_found(client, db, tokens):
    """
    Test requests for non-existing models.

    404 should be returned for any GET/PUT/DELETE request to a non-existing
    model id.
    """
    resp = client.get("/models/1")
    assert resp.status_code == 404

    resp = client.put("/models/1", headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == 404

    resp = client.delete("/models/1", headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == 404
