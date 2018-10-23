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


def test_list_no_token(client, db, models):
    """Only the public model should be listed without a JWT."""
    response = client.get("/models")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['project_id'] is None


def test_list_token(client, db, models, tokens):
    """Both model fixtures should be listed with the JWT claim."""
    response = client.get("/models", headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert response.status_code == 200
    assert len(response.json) == 2


def test_post_no_token(client, db, models):
    """POST resource should require JWT."""
    response = client.post("/models", json={
        'name': "foo",
        'organism_id': 1,
        'project_id': 1,
        'model_serialized': {},
        'default_biomass_reaction': "foo",
    })
    assert response.status_code == 401


def test_post_token(client, db, models, tokens):
    """Allowed to create models with project id in JWT claim."""
    test_model = {
        'name': "Private Model",
        'organism_id': 1,
        'project_id': 4,
        'default_biomass_reaction': "BIOMASS",
        'model_serialized': {"Reactions": [{"GAPDH": "x->y"}]},
    }
    response = client.post("/models", json=test_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert response.status_code == 201

    # Repeating the POST with a project id *not* in claims should be rejected
    test_model['project_id'] = 5
    response = client.post("/models", json=test_model, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert response.status_code == 403


def test_get_no_token(client, db, models):
    """Private model gives impression of not existing without JWT claim."""
    response = client.get("/models/1")
    assert response.status_code == 404


def test_get_token(client, db, models, tokens):
    """Private model can be retrieved with the correct JWT claim."""
    response = client.get("/models/1", headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert response.status_code == 200
    assert response.json['name'] == "Restricted Model"


def test_put_no_token(client, db, models):
    """PUT resource should require JWT."""
    response = client.put("/models/1", json={'name': "Changed"})
    assert response.status_code == 401


def test_put_token(client, db, models, tokens):
    """PUT is allowed with the correct JWT claim."""
    db.session.commit()
    response = client.put("/models/1", json={'name': "Changed"}, headers={
        'Authorization': f"Bearer {tokens['write']}",
    })
    assert response.status_code == 204


def test_delete_no_token(client, db, models):
    """DELETE resource should require JWT."""
    response = client.delete("/models/1")
    assert response.status_code == 401


def test_delete_token(client, db, models, tokens):
    """DELETE is allowed with the correct JWT claim."""
    response = client.delete("/models/1", headers={
        'Authorization': f"Bearer {tokens['admin']}",
    })
    assert response.status_code == 204

    # Verify that the model was deleted
    response = client.get("/models/1", headers={
        'Authorization': f"Bearer {tokens['read']}",
    })
    assert response.status_code == 404
