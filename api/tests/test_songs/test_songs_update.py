from api.db import Database


def test_update_song(
    client, auth_headers: dict, db: Database, song1: dict, song2: dict
):
    song_id = db.create_song(**song1)
    db.create_song_user_link(song_id, "admin")
    result = client.simulate_put(
        f"/songs/{song_id}", headers=auth_headers, json=song2
    )
    assert result.status_code == 200


def test_if_token_missing_then_unauthorized(client, db: Database, song1: dict):
    song_id = db.create_song(**song1)
    result = client.simulate_put(f"/songs/{song_id}", json=song1)
    assert result.status_code == 401


def test_if_song_does_not_exist_then_404(
    client, db: Database, auth_headers: dict, song1: dict, song2: dict
):
    song_id = db.create_song(**song1)
    result = client.simulate_put(
        f"/songs/{song_id + 10}", headers=auth_headers, json=song2
    )
    assert result.status_code == 404


def test_if_malformed_json_then_bad_request(
    client, db: Database, auth_headers: dict, song1
):
    song_id = db.create_song(**song1)
    db.create_song_user_link(song_id, "admin")
    result = client.simulate_put(
        f"/songs/{song_id}", headers=auth_headers, body="qsdmnve"
    )
    assert result.status_code == 400
