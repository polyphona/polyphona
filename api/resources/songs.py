import falcon
from falcon import Request, Response

from ..db import Database
from .parsers import parse_int
from .decorators import authenticated, require_fields


class UserSongsResource:
    def __init__(self, db: Database):
        self.db = db

    def on_get(self, _, resp: Response, username: str):
        if self.db.user_exists(username):
            raise falcon.HTTPNotFound(title=f"No user named {username}.")
        resp.media = self.db.get_songs_by_user(username)


class SongResource:
    def __init__(self, db: Database):
        self.db: Database = db

    @authenticated
    def on_get(self, _, resp: Response, pk: str):
        resp.media = self.db.get_song_by_id(id=parse_int(pk))

    @authenticated
    @require_fields("name", "tracks")
    def on_put(self, req: Request, resp: Response, pk: str):
        self.db.update_song(
            id=parse_int(pk),
            name=req.media["name"],
            tracks=req.media["tracks"],
            username=req.username,
        )
        resp.media = {"id": pk}

    @authenticated
    @require_fields("name", "tracks")
    def on_post(self, req: Request, resp: Response):
        pk = self.db.create_song(
            name=req.media["name"], tracks=req.media["tracks"]
        )
        self.db.create_song_user_link(pk, req.username)
        resp.media = {"id": pk}
        resp.status = falcon.HTTP_201

    @authenticated
    def on_delete(self, req: Request, resp: Response, pk: str):
        self.db.delete_song(id=parse_int(pk), username=req.username)
        resp.status = falcon.HTTP_204
