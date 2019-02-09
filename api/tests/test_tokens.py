import pytest

from api.db import Database


@pytest.fixture
def payload() -> dict:
    return {"username": "smith", "password": "123"}


def test_create_token_wrong_username(client, payload):
    result = client.simulate_post("/tokens", json=payload)
    assert result.status_code == 400


def test_create_token_wrong_password(client, payload):
    result = client.simulate_post("/tokens", json=payload)
    assert result.status_code == 400


@pytest.mark.parametrize("field", ["username", "password"])
def test_if_missing_field_then_bad_request(client, payload, field):
    payload.pop(field)
    result = client.simulate_post("/tokens", json=payload)
    assert result.status_code == 400


def test_if_delete_non_existing_token_then_404(client):
    result = client.simulate_delete("/tokens/doesnotexist")
    assert result.status_code == 404


def test_create_token(client, payload, db: Database):
    user = {"username": "smith", "first_name": "Adam", "last_name": "Smith"}
    db.create_user(**user, password=payload["password"])
    result = client.simulate_post("/tokens", json=payload)
    assert result.status_code == 200
    json = result.json
    assert json["token"]
    assert json["user"] == user


def test_delete_token(client, auth_headers: dict, token: str):
    result = client.simulate_delete(f"/tokens/{token}")
    assert result.status_code == 204
