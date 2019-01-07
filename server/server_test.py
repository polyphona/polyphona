# Use: simply write pytest in command.
# This test must be ran on an empty database, so delete polyphona_db.db if necessary.
#
# Entries to test :
# - GET /users/:username/songs  -OK
# - GET /songs/:id
# - POST /songs                 -OK, maybe also check content of json ?
# - PUT /songs/:id
# - DELETE /songs/:id
# - POST /tokens                -OK
# - DELETE /tokens/:token       -OK
# - POST /users                 -OK
#

from falcon import testing
import pytest

import server


def pytest_namespace():
    return {'token': ''}


test_username = 'smith'
test_first_name = 'smith'
test_last_name = 'smith'
test_password = '123'
test_username_wrong = 'smith2'
test_password_wrong = 'pw'
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
                    "instrumentNumber": 8
                }
            ],
            "startTime": 0,              
            "duration": 10,
            "instrument": "Cello",
        }
    ]
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
                    "instrumentNumber": 8
                }
            ],
            "startTime": 0,              
            "duration": 10,
            "instrument": "Drums",
        }
    ]
}

@pytest.fixture()
def client():
    # Initialize falcon instance
    return testing.TestClient(server.createAPI())


### ## # USERS # ## ###
# Let's create a new user in the blank database
def testCreateUserSmith(client):
    payload = {
        "username": test_username, 
        "first_name": test_first_name, 
        "last_name": test_last_name, 
        "password": test_password
    }
    result = client.simulate_post('/users', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Success
    assert result.status_code == 201
    pass


# Let's try creating a new user with the same username
def testCreateUserSmith2(client):
    payload = {
        "username": test_username, 
        "first_name": "smith2", 
        "last_name": "smith2", 
        "password": test_password_wrong
    }
    result = client.simulate_post('/users', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Rejected because of same username
    assert result.status_code == 403
    pass


### ## # TOKENS # ## ###
def testCreateTokenWrongUsername(client):
    payload = {
        "username": test_username_wrong, 
        "password": test_password
    }
    result = client.simulate_post('/tokens', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400
    pass

def testCreateTokenWrongPassword(client):
    payload = {
        "username": test_username, 
        "password": test_password_wrong
    }
    result = client.simulate_post('/tokens', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400
    pass

def testCreateTokenNoUsername(client):
    payload = {
        "password": test_password
    }
    result = client.simulate_post('/tokens', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400
    pass

def testCreateTokenNoPassword(client):
    payload = {
        "username": test_username, 
    }
    result = client.simulate_post('/tokens', json=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400
    pass

def testCreateTokenCorruptJson(client):
    payload = "{\"username\": \"smith\"}"
    result = client.simulate_post('/tokens', body=payload)
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 400
    pass


def testDeleteTokenWrongToken(client):
    result = client.simulate_delete('/tokens/TOKENNONE')
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 404
    pass

def testCreateToken(client):
    payload = {
        "username": "smith", 
        "password": "123"
    }
    result = client.simulate_post('/tokens', json=payload)
    assert result.status_code == 200
    json_in = result.json
    if len(json_in['token']) == 0:
        print("Empty token returned.")
    assert len(json_in['token']) > 0
    pytest.token = json_in['token']
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    pass


### ## # LIST SONGS # ## ###
# List songs, but there is none
def testListSongsNone(client):
    result = client.simulate_get('/users/{}/songs'.format(test_username))
    json_in = result.json
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    # Success
    assert result.status_code == 200
    assert len(json_in) == 0
    pass


# List songs, but wrong user
def testListSongsWrongUser(client):
    result = client.simulate_get('/users/{}/songs'.format(test_username_wrong))
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 404
    pass


### ## # CREATE SONG # ## ###
# Create song, but invalid token
def testPostSongWrongToken(client):
    parameters = {
        "token": "TOKENNONE"
    }
    result = client.simulate_post('/songs', params=parameters, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass


# Create song, but corrupt payload
def testPostSongCorruptJson(client):
    parameters = {
        "token": pytest.token
    }
    body = "mlkqsd"
    result = client.simulate_post('/songs', params=parameters, body=body)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 400
    pass


# Create song, successful
def testPostSong1(client):
    parameters = {
        "token": pytest.token
    }
    result = client.simulate_post('/songs', params=parameters, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 201
    pass


# Create second song just for the kick of it
def testPostSong2(client):
    parameters = {
        "token": pytest.token
    }
    result = client.simulate_post('/songs', params=parameters, json=test_song_02)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 201
    pass


### ## # LIST SONGS AGAIN # ## ###
# List songs, 2 songs expected
def testListSongsSuccess(client):
    result = client.simulate_get('/users/{}/songs'.format(test_username))
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
    pytest.song_id2 = json_in[2]["id"]
    pass


### ## # Update SONG # ## ###
# Update song, but invalid token
def testPutSongWrongToken(client):
    parameters = {
        "token": "TOKENNONE"
    }
    result = client.simulate_put('/songs/{}'.format(pytest.song_id1), params=parameters, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass


# Update song, but invalid song id
def testPutSongWrongID(client):
    parameters = {
        "token": pytest.token
    }
    result = client.simulate_put('/songs/{}'.format(pytest.song_id1 + 10), params=parameters, json=test_song_01)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass



# Update song, but no right to song id
# TODO: need an additionnal user ....

# Update song, but corrupt json
def testPutSongWrongID(client):
    parameters = {
        "token": pytest.token
    }
    result = client.simulate_put('/songs/{}'.format(pytest.song_id1), params=parameters, body="qsdmnve")
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass





### ## # RETRIEVE SONG # ## ###
def testRetrieveSongWrongToken(client):
    parameters = {
        "token": "TOKENNONE"
    }
    result = client.simulate_get('/songs/IDNONE', params=parameters)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass



### ## # DELETE TOKEN # ## ###
def testDeleteToken(client):
    print("Token = {}".format(pytest.token))
    result = client.simulate_delete('/tokens/{}'.format(pytest.token))
    print("Status: {} ({})".format(result.status, result.status_code))
    print("Result:")
    print(result)
    assert result.status_code == 204
    pass
