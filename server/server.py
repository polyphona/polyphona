# server.py
# use : gunicorn server:app
#
#

import falcon
import json
from uuid import uuid4
import database


app = falcon.API()


class GetSongListRessource(object):
    def on_get(self, req, resp, username):
        if not database.checkUsername(username):
            # Username nor recognized
            resp.status = falcon.HTTP_404
            raise falcon.HTTP_404("Username unknown.")
        json_resp = database.getSongsByUser(username)
        resp.status = falcon.HTTP_200
        resp.body = (json_resp.dump())

get_song_list = GetSongListRessource()
app.add_route('/users/{username}/songs', get_song_list)


class RetrieveSongRessource(object):
    def on_get(self, req, resp, song_id):
        token = req.get_param('token')
        if not database.checkToken(token):
            raise falcon.HTTP_401("Invalid token.")
        json_resp = database.getSongByID(song_id)
        if json_resp is None:
            # Unknown song_id
            resp.status = falcon.HTTP_404
            raise falcon.HTTP_404("song_id unknown.")
        resp.status = falcon.HTTP_200
        resp.body = (json_resp.dump())

retreive_song = RetrieveSongRessource()
app.add_route('/songs/{song_id}', retreive_song)


class CreateSongRessource(object):
    def on_post(self, req, resp):
        token = req.get_param('token')
        if database.checkToken(token) is None:
            raise falcon.HTTP_401("Invalid token.")
        try:
            json_in.loads(req.stream.read(self._CHUNK_SIZE_BYTES))
        except:
            raise falcon.HTTP_400("unreadable json.")
        if 'name' not in json_in.keys():
            raise falcon.HTTP_400("Missing name field.")
        if 'tracks' not in json_in.keys():
            raise falcon.HTTP_400("Missing tracks field.")
        song_id = database.createSong(json_in["name"], json_in["tracks"])
        if song_id is None:
            raise falcon.HTTP_500("Server error: could not create song.")
        if not database.createSongUserLink(song_id, json_in["username"]):
            raise falcon.HTTP_500("Server error: could not link song with user.")
        resp.status = falcon.HTTP_200

create_song = CreateSongRessource()
app.add_route('/songs', create_song)


class SongRessource(object):
    def on_put(self, req, resp, song_id):
        token = req.get_param('token')
        if database.IsTokenValid(token) is None:
            raise falcon.HTTP_401("Invalid token.")
        if database.getSongById(song_id) is None:
            raise falcon.HTTP_400("Invalid song id.")
        try:
            json_in.loads(req.stream.read(self._CHUNK_SIZE_BYTES))
        except:
            raise falcon.HTTP_400("unreadable json.")
        if 'name' not in json_in.keys():
            raise falcon.HTTP_400("Missing name field.")
        if 'tracks' not in json_in.keys():
            raise falcon.HTTP_400("Missing tracks field.")
        if not database.updateSong(song_id, json_in["name"], json_in["tracks"]):
            raise falcon.HTTP_500("Server error: could not update song.")
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, song_id):
        token = req.get_param('token')
        username = database.IsTokenValid(token)
        if username is None:
            raise falcon.HTTP_401("Invalid token.")
        songs = database.getSongsByUser(username)
        if songs is None:
            raise falcon.HTTP_500("Server error: username disappeared.")
        song_id_list = []
        for song in songs:
            song_id_list.append(song["song_id"])
        if song_id not in song_id_list:
            raise falcon.HTTP_403("No rights to this song.")
        if not database.deleteSong(song_id):
            raise falcon.HTTP_500("Server error: could not delete song.")
        resp.status = falcon.HTTP_200

update_delete_song = SongRessource()
app.add_route('/songs/{song_id}', update_delete_song)


class CreateTokenRessource(object):
    def on_post(self, req, resp):
        try:
            json_in.loads(req.stream.read(self._CHUNK_SIZE_BYTES))
        except:
            raise falcon.HTTP_400("unreadable json.")
        if 'username' not in json_in.keys():
            raise falcon.HTTP_400("Missing username field.")
        if 'password' not in json_in.keys():
            raise falcon.HTTP_400("Missing password field.")
        if not database.checkUser(json_in["username"], json_in["password"]):
            raise falcon.HTTP_406("Invalid login information.")
        new_token = str(uuid4())
        if database.IsTokenValid(new_token) is not None:
            new_token = str(uuid4())
        if database.IsTokenValid(new_token) is not None:
            raise falcon.HTTP_508("Cannot generate token.")
        if not database.createToken(username, new_token):
            raise falcon.HTTP_500("Failed to validate token (unexcepted).")
        json_out = {
            "token" : new_token, 
            "user" : database.getUserInfo(json_in["username"])
        }
        resp.body = json.dumps(json_out, ensure_ascii=False)
        resp.status = falcon.HTTP_200

create_token = CreateTokenRessource()
app.add_route('/tokens', create_token)


class DeleteTokenRessource(object):
    def on_delete(self, req, resp):
        if database.IsTokenValid(new_token) is None:
            raise falcon.HTTP_404("Invalid token.")
        if not database.deleteToken(token):
            raise falcon.HTTP_500("Failed to delete token.")
        resp.status = falcon.HTTP_204

delete_token = DeleteTokenRessource()
app.add_route('/tokens/{token}', delete_token)




"""
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
"""
