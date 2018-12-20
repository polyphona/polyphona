# Use: simply write pytest in command.
# This test must be ran on an empty database, so delete polyphona_db.db if necessary.

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


### ## # SONGS # ## ###
def testRetrieveSong(client):
    parameters = {
        "token": "TOKENNONE"
    }
    result = client.simulate_get('/songs/IDNONE', params=parameters)
    print("Status: {} ({})".format(result.status, result.status_code))
    assert result.status_code == 401
    pass

def testPostSongCorruptJson(client):
    parameters = {
        "token": "TOKENNONE"
    }
    body = "mlkqsd"
    result = client.simulate_post('/songs', params=parameters, body=body)
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
