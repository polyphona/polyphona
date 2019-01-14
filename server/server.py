# server.py
# use : gunicorn server:app
# api : https://hackmd.io/eNiNVR6eR1mJH2kOebtE5g#
#

import falcon
import json
from uuid import uuid4
import database



def validate_json(req):
    try:
        json_in = json.loads(req.stream.read().decode('utf-8'))
    except json.JSONDecodeError:
        raise falcon.HTTPError(falcon.HTTP_400, "unreadable json.")
    else:
        return json_in


def validate_int(value):
    rtn = 0
    try:
        rtn = int(value)
    except:
        raise falcon.HTTPError(falcon.HTTP_400, "Invalid song ID.")
    return rtn



class UserResource(object):

    def on_post(self, req, resp):
        json_in = validate_json(req)

        # Check validity of request
        for field in 'username', 'first_name', 'last_name', 'password':
            if field not in json_in:
                raise falcon.HTTPError(falcon.HTTP_400, 'Missing {} field.'.format(field))

        if not database.is_user_name_free(json_in['username']):
            raise falcon.HTTPError(falcon.HTTP_400, "Username already taken.")
        if not database.create_user(json_in['username'], json_in['first_name'], json_in['last_name'],
                                    json_in['password']):
            raise falcon.HTTPError(falcon.HTTP_500, "Unexpected server error.")

        resp.status = falcon.HTTP_201



class GetSongListResource(object):

    def on_get(self, req, resp, username):
        # Check validity of request
        if database.is_user_name_free(username):
            # Username nor recognized
            raise falcon.HTTPError(falcon.HTTP_404, "Username unknown.")

        # Generate response
        json_resp = database.get_songs_by_user(username)
        resp.body = json.dumps(json_resp)
        resp.status = falcon.HTTP_200



class SongResource(object):
    def on_get(self, req, resp, song_id_str):
        song_id = validate_int(song_id_str)
        token = req.get_param('token')

        # Check validity of request
        if not database.is_token_valid(token):
            raise falcon.HTTPError(falcon.HTTP_401, "Invalid token.")
        song = database.get_song_by_id(song_id)
        if song is None:
            # Unknown song_id
            resp.status = falcon.HTTP_404
            raise falcon.HTTPError(falcon.HTTP_404, "song_id unknown.")

        # Generate response
        resp.body = json.dumps(song)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, song_id_str):
        song_id = validate_int(song_id_str)
        token = req.get_param('token')

        # Check validity of request
        username = database.is_token_valid(token)
        if username is None:
            raise falcon.HTTPError(falcon.HTTP_401, "Invalid token.")

        songs = database.get_songs_by_user(username)
        song_id_list = [song["id"] for song in songs]
        if song_id not in song_id_list:
            raise falcon.HTTPError(falcon.HTTP_404, "Song ID unknown.")

        json_in = validate_json(req)
        for field in 'name', 'tracks':
            if field not in json_in.keys():
                raise falcon.HTTPError(falcon.HTTP_400, "Missing {} field.".format(field))

        # Process request
        database.update_song(song_id, json_in["name"], json.dumps(json_in["tracks"]))
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        token = req.get_param('token')

        # Check validity of request
        if database.is_token_valid(token) is None:
            raise falcon.HTTPError(falcon.HTTP_401, "Invalid token.")
        json_in = validate_json(req)
        if 'name' not in json_in.keys():
            raise falcon.HTTPError(falcon.HTTP_400, "Missing name field.")
        if 'tracks' not in json_in.keys():
            raise falcon.HTTPError(falcon.HTTP_400, "Missing tracks field.")

        # Process request
        song_id = database.create_song(json_in["name"], json.dumps(json_in["tracks"]))
        database.create_song_user_link(song_id, database.is_token_valid(token))
        resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, song_id_str):
        song_id = validate_int(song_id_str)
        token = req.get_param('token')

        # Check validity of request
        username = database.is_token_valid(token)
        if username is None:
            raise falcon.HTTPError(falcon.HTTP_401, "Invalid token.")
        songs = database.get_songs_by_user(username)
        song_id_list = []
        for song in songs:
            song_id_list.append(song["id"])
        if song_id not in song_id_list:
            # Song ID does not belong to user
            raise falcon.HTTPError(falcon.HTTP_404, "Song ID unknown.")

        # Process request
        database.delete_song(song_id)
        resp.status = falcon.HTTP_204



class TokenResource(object):

    def on_post(self, req, resp):
        json_in = validate_json(req)

        # Check validity of request
        if 'username' not in json_in.keys():
            raise falcon.HTTPError(falcon.HTTP_400, "Missing username field.")
        if 'password' not in json_in.keys():
            raise falcon.HTTPError(falcon.HTTP_400, "Missing password field.")
        if not database.check_user(json_in["username"], json_in["password"]):
            raise falcon.HTTPError(falcon.HTTP_400, "Invalid login information.")

        # Try and generate a new token
        new_token = str(uuid4())
        if database.is_token_valid(new_token) is not None:
            new_token = str(uuid4())
        if database.is_token_valid(new_token) is not None:
            raise falcon.HTTPError(falcon.HTTP_508, "Cannot generate token.")
        if not database.create_token(json_in["username"], new_token):
            raise falcon.HTTPError(falcon.HTTP_500, "Failed to validate token (unexcepted).")

        # Generate response
        json_out = {
            "token": new_token,
            "user": database.get_user_info(json_in["username"])
        }
        resp.body = json.dumps(json_out, ensure_ascii=False)
        resp.status = falcon.HTTP_200


    def on_delete(self, req, resp, token):
        if not database.delete_token(token):
            raise falcon.HTTPError(falcon.HTTP_404, "Invalid token.")
        resp.status = falcon.HTTP_204



def create_api():
    app = falcon.API()

    database.create_database_table()

    user_resource = UserResource()
    app.add_route('/users/', user_resource)

    get_song_list = GetSongListResource()
    app.add_route('/users/{username}/songs', get_song_list)

    update_delete_song = SongResource()
    app.add_route('/songs/{song_id_str}', update_delete_song)
    app.add_route('/songs/', update_delete_song)

    token_resource = TokenResource()
    app.add_route('/tokens/{token}', token_resource)
    app.add_route('/tokens/', token_resource)

    return app


app = create_api()
