# server.py
# use : gunicorn server:app
#
# DB requets :
#  - All songs from user. -> list of song names
#  - Give me this song. -> dict (json)
#  - Is user valid ? -> boolean
#  - Create song : user, json -> None (may fail if invalid user or song name already taken)
#  - Create user : user, password -> None (may fail if user name is already taken)
#

import falcon
import json
#import database


class GetSongListRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        resp.status = falcon.HTTP_200
        # DB request
        resp.body = ('Hello world ! getsonglist\n\n')

class GetSongRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        resp.status = falcon.HTTP_200
        # DB request
        resp.body = ('Hello world ! getsong\n\n')

class CreateSongRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        resp.status = falcon.HTTP_200
        body = req.stream.read()
        resp.body = ('Hello world ! createsong\n\n')
        if not body:
            print("Nothing to read from the CreateSong request.")
            pass
        try:
            json_file = json.loads(body.decode('utf-8'))
        except(ValueError, UnicodeDecodeError):
            print("Data formating error.")
        # DB request
#        database.addSong(json_file, used_id)

class CreateUserRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        password = req.get_param('password')
        resp.status = falcon.HTTP_200
        # DB request
        resp.body = ('Hello world ! createsong\n\n')


app = falcon.API()

get_song_list = GetSongListRessource()
app.add_route('/get_song_list', get_song_list)

get_song = GetSongRessource()
app.add_route('/get_song', get_song)

create_song = CreateSongRessource()
app.add_route('/create_song', create_song)

create_user = CreateUserRessource()
app.add_route('/create_user', create_user)


"""
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
"""