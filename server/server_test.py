# Use: simply write pytest in command.
# This test must be ran on an empty database, so delete polyphona_db.db if necessary.
#
# Entries to test :
# - GET /users/:username/songs  -OK
# - GET /songs/:id              -OK
# - POST /songs                 -OK, maybe also check content of json ?
# - PUT /songs/:id              -OK
# - DELETE /songs/:id           -OK
# - POST /tokens                -OK
# - DELETE /tokens/:token       -OK
# - POST /users                 -OK
#

import json
import pytest
from falcon import testing
from falcon import testing
from database import *
import os

import server


def pytest_namespace():
    return {"token": ""}


database_path = "fake_db.db"
test_username = "smith"
test_first_name = "Smithy"
test_last_name = "Smith"
test_password = "123"
test_username_wrong = "smith2"
test_password_wrong = "pw"
test_song_01 = {
    "name": "Song 01",
    "tracks": [
        {
            "id": 1,
            "name": "Cello",
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
            "instrument": "Cello",
        }
    ],
}
test_song_02 = {
    "name": "Song 02",
    "tracks": [
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
test_song_03 = {
    "name": "Song 03",
    "tracks": [
        {
            "id": 1,
            "name": "Dibs",
            "isMuted": True,
            "notes": [
                {
                    "midi": 10,
                    "time": 10,
                    "note": "A2",
                    "velocity": 64,
                    "duration": 16,
                    "instrumentNumber": 8,
                },
                {
                    "midi": 10,
                    "time": 10,
                    "note": "A3",
                    "velocity": 64,
                    "duration": 16,
                    "instrumentNumber": 8,
                },
            ],
            "startTime": 0,
            "duration": 10,
            "instrument": "Shotagonu",
        }
    ],
}
try:
    os.remove(database_path)
except:
    pass


def setup_module(module):
    create_database_table(database_path)


@pytest.fixture()
def client():
    # Initialize falcon instance
    return testing.TestClient(server.create_api(database_path))


### ## # USERS # ## ###
# Let's create a new user in the blank database
def test_create_user_smith(client):
    payload = {
        "username": test_username,
        "first_name": test_first_name,
        "last_name": test_last_name,
        "password": test_password,
    }
    result = client.simulate_post("/users", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Success
    assert result.status_code == 201


# Let's try creating a new user with the same username
def test_create_user_smith2(client):
    payload = {
        "username": test_username,
        "first_name": "smith2",
        "last_name": "smith2",
        "password": test_password_wrong,
    }
    result = client.simulate_post("/users", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Rejected because of same username
    assert result.status_code == 400


### ## # TOKENS # ## ###
def test_create_token_wrong_username(client):
    payload = {"username": test_username_wrong, "password": test_password}
    result = client.simulate_post("/tokens", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400


def test_create_token_wrong_password(client):
    payload = {"username": test_username, "password": test_password_wrong}
    result = client.simulate_post("/tokens", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400


def test_create_token_no_username(client):
    payload = {"password": test_password}
    result = client.simulate_post("/tokens", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400


def test_create_token_no_password(client):
    payload = {"username": test_username}
    result = client.simulate_post("/tokens", json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400


def test_create_token_corrupt_json(client):
    payload = '{"username": "smith"}'
    result = client.simulate_post("/tokens", body=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400


def test_delete_token_wrong_token(client):
    result = client.simulate_delete("/tokens/TOKENNONE")
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 404


def test_create_token(client):
    payload = {"username": "smith", "password": "123"}
    result = client.simulate_post("/tokens", json=payload)
    assert result.status_code == 200
    json_in = result.json
    if len(json_in["token"]) == 0:
        print("Empty token returned.")
    assert len(json_in["token"]) > 0
    pytest.token = json_in["token"]
    assert json_in["user"]["username"] == test_username
    assert json_in["user"]["first_name"] == test_first_name
    assert json_in["user"]["last_name"] == test_last_name
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)


### ## # LIST SONGS # ## ###
# List songs, but there is none
def test_list_songs_none(client):
    result = client.simulate_get("/users/{}/songs".format(test_username))
    json_in = result.json
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Success
    assert result.status_code == 200
    assert len(json_in) == 0


# List songs, but wrong user
def test_list_songs_wrong_user(client):
    result = client.simulate_get("/users/{}/songs".format(test_username_wrong))
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 404


### ## # CREATE SONG # ## ###
# Create song, but invalid token
def test_post_song_wrong_token(client):
    headers = {"Authorization": "Token " + "TOKENNONE"}
    result = client.simulate_post("/songs", headers=headers, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401


# Create song, but corrupt payload
def test_post_song_corrupt_json(client):
    headers = {"Authorization": "Token " + pytest.token}
    body = "mlkqsd"
    result = client.simulate_post("/songs", headers=headers, body=body)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 400


# Create song, successful
def test_post_song_1(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_post("/songs", headers=headers, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 201


# Create second song just for the kick of it
def test_post_song_2(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_post("/songs", headers=headers, json=test_song_02)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 201


### ## # LIST SONGS AGAIN # ## ###
# List songs, 2 songs expected
def test_list_songs_success(client):
    result = client.simulate_get("/users/{}/songs".format(test_username))
    json_in = result.json
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Success
    assert result.status_code == 200
    assert len(json_in) == 2
    song_names = [json_in[0]["name"], json_in[1]["name"]]
    assert test_song_01["name"] in song_names
    assert test_song_02["name"] in song_names
    pytest.song_id1 = json_in[0]["id"]
    pytest.song_id2 = json_in[1]["id"]


# Retrieve song, check it's been well saved
def test_retrieve_song_check_create(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_get("/songs/{}".format(pytest.song_id2), headers=headers)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 200
    json_dict = result.json
    del json_dict["created"]
    del json_dict["updated"]
    del json_dict["id"]
    assert json_dict == test_song_02


### ## # Update SONG # ## ###
# Update song, but invalid token
def test_put_song_wrong_token(client):
    headers = {"Authorization": "Token " + "TOKENNONE"}
    result = client.simulate_put(
        "/songs/{}".format(pytest.song_id2), headers=headers, json=test_song_01
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401


# Update song, but invalid song id
def test_put_song_wrong_id(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_put(
        "/songs/{}".format(pytest.song_id2 + 10), headers=headers, json=test_song_01
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 404


# Update song, but no right to song id
# TODO: need an additionnal user ....


def test_update_song_corrupt_json(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_put(
        "/songs/{}".format(pytest.song_id2), headers=headers, body="qsdmnve"
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 400


# Update song, success
def test_put_song(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_put(
        "/songs/{}".format(pytest.song_id2), headers=headers, json=test_song_03
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 200


### ## # DELETE SONG # ## ###
# Delete song, wrong token
def test_delete_song_wrong_token(client):
    headers = {"Authorization": "Token " + "TOKENNONE"}
    result = client.simulate_delete(
        "/songs/{}".format(pytest.song_id1), headers=headers
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401


# Delete song, wrong song id
def test_delete_song_wrong_token(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_delete(
        "/songs/{}".format(pytest.song_id1 + 100), headers=headers
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 404


# Delete song, success
def test_delete_song(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_delete(
        "/songs/{}".format(pytest.song_id1), headers=headers
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 204


### ## # RETRIEVE SONG # ## ###
# Retrieve song, wrong token
def test_retrieve_song_wrong_token(client):
    headers = {"Authorization": "Token " + "TOKENNONE"}
    result = client.simulate_get("/songs/{}".format(pytest.song_id1), headers=headers)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401


# Retrieve song, wrong song ID
def test_retrieve_song_wrong_id(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_get(
        "/songs/{}".format(pytest.song_id1 + 100), headers=headers
    )
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 404


# Retrieve song, old song ID
def test_retrieve_song_old_id(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_get("/songs/{}".format(pytest.song_id1), headers=headers)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 404


# Retrieve song, success
def test_retrieve_song(client):
    headers = {"Authorization": "Token " + pytest.token}
    result = client.simulate_get("/songs/{}".format(pytest.song_id2), headers=headers)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 200
    json_dict = result.json
    del json_dict["created"]
    del json_dict["updated"]
    del json_dict["id"]
    assert json_dict == test_song_03


### ## # DELETE TOKEN # ## ###
def test_delete_token(client):
    print("Token = {}".format(pytest.token))
    result = client.simulate_delete("/tokens/{}".format(pytest.token))
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 204
