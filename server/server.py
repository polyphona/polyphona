# server.py
# use : gunicorn server:app
# api : https://hackmd.io/eNiNVR6eR1mJH2kOebtE5g#
#

import falcon
import json
from uuid import uuid4
import database


def raise_error_macro(error_code, str):
    print(str)
    raise falcon.HTTPError(error_code, str)
    pass


def extract_json(req):
    try:
        json_in = json.loads(req.stream.read().decode('utf-8'))
    except json.JSONDecodeError:
        raise_error_macro(falcon.HTTP_400, "unreadable json.")
    else:
        return json_in


def strToInt(str):
    rtn = 0
    try:
        rtn = int(str)
    except:
        raise_error_macro(falcon.HTTP_400, "Invalid song ID.")
    return rtn

class UserResource(object):

    def on_post(self, req, resp):
        json_in = extract_json(req)

        for field in 'username', 'first_name', 'last_name', 'password':
            if field not in json_in:
                raise_error_macro(400, f'Missing {field} field.')

        if not database.is_user_name_free(json_in['username']):
            raise_error_macro(falcon.HTTP_403, "Username already taken.")
        if not database.create_user(json_in['username'], json_in['first_name'], json_in['last_name'],
                                    json_in['password']):
            raise_error_macro(falcon.HTTP_500, "Unexpected server error.")

        resp.status = falcon.HTTP_201


class GetSongListResource(object):

    def on_get(self, req, resp, username):
        if database.is_user_name_free(username):
            # Username nor recognized
            resp.status = falcon.HTTP_404
            raise_error_macro(falcon.HTTP_404, "Username unknown.")
        json_resp = database.get_songs_by_user(username)
        if json_resp is None:
            raise_error_macro(falcon.HTTP_500, "Server error: failed to retreive songs.")
        resp.status = falcon.HTTP_200
        resp.body = (json.dumps(json_resp))


class SongResource(object):
    def on_get(self, req, resp, song_id_str):
        song_id = strToInt(song_id_str)
        token = req.get_param('token')
        if not database.is_token_valid(token):
            raise_error_macro(falcon.HTTP_401, "Invalid token.")
        json_resp = database.get_song_by_id(song_id)
        if json_resp is None:
            # Unknown song_id
            resp.status = falcon.HTTP_404
            raise_error_macro(falcon.HTTP_404, "song_id unknown.")
        resp.status = falcon.HTTP_200
        resp.body = (json.dumps(json_resp))

    def on_put(self, req, resp, song_id_str):
        song_id = strToInt(song_id_str)
        token = req.get_param('token')
        username = database.is_token_valid(token)
        if username is None:
            raise_error_macro(falcon.HTTP_401, "Invalid token.")
        songs = database.get_songs_by_user(username)
        if songs is None:
            raise_error_macro(falcon.HTTP_500, "Server error: username disappeared.")
        song_id_list = []
        for song in songs:
            song_id_list.append(song["id"])
        if song_id not in song_id_list:
            raise_error_macro(falcon.HTTP_404, "Song ID unknown.")
        json_in = extract_json(req)
        if 'name' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing name field.")
        if 'tracks' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing tracks field.")
        if not database.update_song(song_id, json_in["name"], json.dumps(json_in["tracks"])):
            raise_error_macro(falcon.HTTP_500, "Server error: could not update song.")
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        token = req.get_param('token')
        if database.is_token_valid(token) is None:
            raise_error_macro(falcon.HTTP_401, "Invalid token.")
        json_in = extract_json(req)
        if 'name' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing name field.")
        if 'tracks' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing tracks field.")
        song_id = database.create_song(json_in["name"], json.dumps(json_in["tracks"]))
        if song_id is None:
            raise_error_macro(falcon.HTTP_500, "Server error: could not create song.")
        if not database.create_song_user_link(song_id, database.is_token_valid(token)):
            raise_error_macro(falcon.HTTP_500, "Server error: could not link song with user.")
        resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, song_id_str):
        song_id = strToInt(song_id_str)
        token = req.get_param('token')
        username = database.is_token_valid(token)
        if username is None:
            raise_error_macro(falcon.HTTP_401, "Invalid token.")
        songs = database.get_songs_by_user(username)
        if songs is None:
            raise_error_macro(falcon.HTTP_500, "Server error: username disappeared.")
        song_id_list = []
        for song in songs:
            song_id_list.append(song["id"])
        if song_id not in song_id_list:
            raise_error_macro(falcon.HTTP_404, "Song ID unknown.")
        if not database.delete_song(song_id):
            raise_error_macro(falcon.HTTP_500, "Server error: could not delete song.")
        resp.status = falcon.HTTP_204


class TokenResource(object):

    def on_post(self, req, resp):
        json_in = extract_json(req)
        if 'username' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing username field.")
        if 'password' not in json_in.keys():
            raise_error_macro(falcon.HTTP_400, "Missing password field.")
        if not database.check_user(json_in["username"], json_in["password"]):
            raise_error_macro(falcon.HTTP_400, "Invalid login information.")
        new_token = str(uuid4())
        if database.is_token_valid(new_token) is not None:
            new_token = str(uuid4())
        if database.is_token_valid(new_token) is not None:
            raise_error_macro(falcon.HTTP_508, "Cannot generate token.")
        if not database.create_token(json_in["username"], new_token):
            raise_error_macro(falcon.HTTP_500, "Failed to validate token (unexcepted).")
        json_out = {
            "token": new_token,
            "user": database.get_user_info(json_in["username"])
        }
        resp.body = json.dumps(json_out, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, token):
        if database.is_token_valid(token) is None:
            raise_error_macro(falcon.HTTP_404, "Invalid token.")
        if not database.delete_token(token):
            raise_error_macro(falcon.HTTP_500, "Failed to delete token.")
        resp.status = falcon.HTTP_204


def createAPI():
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


app = createAPI()

"""
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
"""
