import falcon
from falcon import Request, Response

from ..db import Database
from .parsers import parse_int
from .decorators import authenticated, require_fields


class GetSongListResource:
    def __init__(self, db: Database):
        self.db = db

    def on_get(self, req: Request, resp: Response, username: str):
        if self.db.user_exists(username):
            raise falcon.HTTPNotFound(title=f"No user named {username}.")
        resp.media = self.db.get_songs_by_user(username)


class SongResource:
    def __init__(self, db: Database):
        self.db: Database = db

    @authenticated
    def on_get(self, _, resp: ResourceWarning, song_id_str: str):
        song_id = parse_int(song_id_str)

        song = self.db.get_song_by_id(song_id)
        if song is None:
            raise falcon.HTTPNotFound(title=f"Song {song_id} does not exist.")

        resp.media = song

    @authenticated
    @require_fields("name", "tracks")
    def on_put(self, req: Request, resp: Response, song_id_str):
        song_id = parse_int(song_id_str)
        songs = self.db.get_songs_by_user(req.username)
        song_id_list = [song["id"] for song in songs]
        if song_id not in song_id_list:
            raise falcon.HTTPNotFound(title=f"Song {song_id} does not exist.")

        data = req.media
        self.db.update_song(song_id, data["name"], data["tracks"])

    @authenticated
    @require_fields("name", "tracks")
    def on_post(self, req: Request, resp: Response):
        data = req.media
        song_id = self.db.create_song(data["name"], data["tracks"])
        self.db.create_song_user_link(song_id, req.username)
        resp.status = falcon.HTTP_201

    @authenticated
    def on_delete(self, req: Request, resp: Response, song_id_str):
        song_id = parse_int(song_id_str)

        songs = self.db.get_songs_by_user(req.username)
        if song_id not in map(lambda song: song["id"], songs):
            raise falcon.HTTPNotFound(title="Song ID unknown.")

        self.db.delete_song(song_id)
        resp.status = falcon.HTTP_204
