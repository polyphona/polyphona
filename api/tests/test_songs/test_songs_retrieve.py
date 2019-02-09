from api.db import Database


def test_retrieve_song(client, db: Database, auth_headers: dict, song1: dict):
    song_id = db.create_song(**song1)
    result = client.simulate_get(f"/songs/{song_id}", headers=auth_headers)
    assert result.status_code == 200
    data = result.json
    del data["created"]
    del data["updated"]
    del data["id"]
    assert data == song1


def test_if_token_missing_then_unauthorized(client, db: Database, song1):
    song_id = db.create_song(**song1)
    result = client.simulate_get(f"/songs/{song_id}")
    assert result.status_code == 401


def test_if_song_does_not_exist_then_not_found(client, auth_headers):
    result = client.simulate_get("/songs/1", headers=auth_headers)
    assert result.status_code == 404

