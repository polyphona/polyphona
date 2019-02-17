def test_if_missing_token_then_unauthorized(client, song1):
    result = client.simulate_post("/songs", json=song1)
    assert result.status_code == 401


def test_if_bad_json_then_bad_request(client, auth_headers):
    result = client.simulate_post("/songs", headers=auth_headers, body="mlkqds")
    assert result.status_code == 400


def test_create_song(client, auth_headers: dict, song1: dict, song2: dict):
    for song in (song1, song2):
        result = client.simulate_post("/songs", headers=auth_headers, json=song)
        assert result.status_code == 201
