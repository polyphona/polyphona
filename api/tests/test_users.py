import pytest


@pytest.fixture
def payload(example_user) -> dict:
    return {**example_user, "password": "123"}


def test_create_user(client, payload):
    result = client.simulate_post("/users", json=payload)
    assert result.status_code == 201


def test_if_username_taken_then_bad_request(client, payload):
    result = client.simulate_post("/users", json=payload)
    assert result.status_code == 201

    result = client.simulate_post("/users", json=payload)
    assert result.status_code == 400
