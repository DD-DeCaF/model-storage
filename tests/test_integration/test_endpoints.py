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

import pytest


def test_models_get(client, session, model, tokens):
    """Test the /models GET API supposed to return all models in the DB."""
    resp = client.get("/models", headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert resp.status_code == 200
    assert len(resp.json) == 1


def test_models_post(client, session, tokens, e_coli_core):
    """Test the /models POST API supposed to post a single model to the DB."""
    new_model = {
        "name": "iML12311",
        "model_serialized": e_coli_core,
        "organism_id": 1,
        "project_id": 4,
        "default_biomass_reaction": "BIOMASS_Ecoli_core_w_GAM",
        "preferred_map_id": 1
    }

    resp = client.post("/models", json=new_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == 201
    assert resp.headers["Location"].endswith(f"/models/{resp.json['id']}")


@pytest.mark.parametrize("url, code", [
    ("/models/1", 200),
    ("/models/10", 404),
])
def test_indvmodel_get(client, session, model, tokens, url, code):
    """Test the /models/<id> GET API supposed to get a single model by ID."""
    resp = client.get(url, headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert resp.status_code == code


@pytest.mark.parametrize("url, code", [
    ("/models/1", 204),
    ("/models/10", 404),
])
def test_indvmodel_put(client, session, model, tokens, url, code, e_coli_core):
    """Test the /models/<id> PUT API supposed to modify a single model by ID."""
    updated_model = {
        "name": "e_coli_core",
        "model_serialized": e_coli_core,
        "organism_id": 1,
        "project_id": 1,
        "default_biomass_reaction": "BIOMASS_Ecoli_core_w_GAM",
        "preferred_map_id": 1
    }
    resp = client.put(url, json=updated_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert resp.status_code == code


@pytest.mark.parametrize("url, code", [
    ("/models/1", 204),
    ("/models/10", 404),
])
def test_indvmodel_delete(client, session, model, tokens, url, code):
    """Test the /models/<id> PUT API supposed to remove a single model by ID."""
    resp = client.delete(url, headers={
        'Authorization': f"Bearer {tokens['admin']}",
    })
    assert resp.status_code == code
