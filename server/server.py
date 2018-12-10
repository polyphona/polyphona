# server.py
# use : gunicorn server:app
#
# DB requets :
#  - Create user : username (unique), first name, last name, password
#    -> create new user instance
#    -> true or false (false if the username is already taken)
#  - Check username : username
#    -> true or false (just check if the username is taken)
#  - Check user : username, password
#    -> true or false
#
#  - Check token : token
#    -> username or None
#  - Check user token : user
#    -> token or None (return token if there already is a token for this user)
#  - Create token : username, token
#    -> True or False (token taken or wrong username)
#
#  - Get song by id : song_id
#    -> dict or None
#  - Get songs by user : username
#    -> list of dict or None
#
#  - Create song : username, song_name
#    -> song_id or None
#  - Update song : username
#    -> list of dict or None
#  - Delete song : song_id
#    -> True or False
#

import falcon
import json
#import database


class GetSongListRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        resp.status = falcon.HTTP_200
#        song_list = database.songsByUser(user_id)
        resp.body = ('Hello world ! getsonglist\n\n')

class GetSongRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        song_name = req.get_param('song_name')
        resp.status = falcon.HTTP_200
#        raw_json = database.getSongByTitle(song_name)
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
#        database.addSong(used_id, json_file)

class CreateUserRessource(object):
    def on_get(self, req, resp):
        user_id = req.get_param('user_id')
        password = req.get_param('password')
        resp.status = falcon.HTTP_200
#        database.addUser(user_id, password)
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