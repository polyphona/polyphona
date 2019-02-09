import pytest

from api.db import Database


@pytest.fixture
def username(db: Database, example_user) -> dict:
    db.create_user(**example_user, password="foo")
    return example_user["username"]


def test_list_songs(client, db: Database, username):
    result = client.simulate_get(f"/users/{username}/songs")
    assert result.status_code == 200


def test_list_is_empty_if_no_songs(client, username):
    result = client.simulate_get(f"/users/{username}/songs")
    assert result.status_code == 200
    assert len(result.json) == 0


def test_if_user_does_not_exist_then_404(client):
    result = client.simulate_get("/users/doesnotexist/songs")
    assert result.status_code == 404


def test_with_existing_songs(client, username, db: Database, song1, song2):
    for song in song1, song2:
        song_id = db.create_song(**song)
        db.create_song_user_link(song_id=song_id, username=username)

    result = client.simulate_get(f"/users/{username}/songs")
    assert result.status_code == 200
    assert [(song["id"], song["name"]) for song in result.json] == [
        (1, song1["name"]),
        (2, song2["name"]),
    ]
