import pytest
from falcon.testing import TestClient

from api.db import Database
from api.server import create_api


@pytest.fixture
def db() -> Database:
    test_db = Database("test.db")
    test_db.generate_schema()
    try:
        yield test_db
    finally:
        test_db.remove()


@pytest.fixture
def client(db: Database) -> TestClient:
    return TestClient(create_api(db))


@pytest.fixture
def example_user() -> dict:
    return {"username": "smith", "first_name": "Adam", "last_name": "Smith"}


@pytest.fixture
def token() -> str:
    return "1234"


@pytest.fixture
def auth_headers(db: Database, example_user: dict, token: str) -> dict:
    db.create_user(
        username="admin",
        first_name="admin",
        last_name="admin",
        password="admin",
    )
    db.create_token(username="admin", token=token)
    return {"Authorization": f"Token {token}"}


@pytest.fixture
def song2_payload(db: Database) -> dict:
    return {
        "name": "Song 02",
        "data": [
            {
                "id": 1,
                "name": "Drums",
                "isMuted": False,
                "notes": [
                    {
                        "midi": 10,
                        "time": 10,
                        "note": "A2",
                        "velocity": 64,
                        "duration": 16,
                        "instrumentNumber": 8,
                    }
                ],
                "startTime": 0,
                "duration": 10,
                "instrument": "Drums",
            }
        ],
    }
