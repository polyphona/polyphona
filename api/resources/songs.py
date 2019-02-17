import falcon
from falcon import Request, Response

from ..db import Database
from .parsers import parse_int
from .decorators import authenticated, require_fields


class UserSongsResource:
    """Resource to access a user's list of songs.
    
    Parameters
    ----------
    db : Database
    """

    def __init__(self, db: Database):
        self.db = db

    @authenticated
    def on_get(self, _, resp: Response, username: str):
        """Return a user's list of songs.

        Requires authentication.

        Raises
        ------
        HTTPNotFound :
            If user ``username`` does not exist.
        """
        if self.db.user_exists(username):
            raise falcon.HTTPNotFound(title=f"No user named {username}.")
        resp.media = self.db.get_songs_by_user(username)


class SongResource:
    """Resource to access or modify songs.
    
    Parameters
    ----------
    db : Database
    """

    def __init__(self, db: Database):
        self.db: Database = db

    @authenticated
    def on_get(self, _, resp: Response, pk: str):
        """Return a song by ID."""
        resp.media = self.db.get_song_by_id(id=parse_int(pk))

    @authenticated
    @require_fields("name", "tracks")
    def on_put(self, req: Request, resp: Response, pk: str):
        """Modify a song.

        Requires authentication.
        """
        id: int = parse_int(pk)
        self.db.update_song(
            id=id,
            name=req.media["name"],
            tracks=req.media["tracks"],
            username=req.username,
        )
        resp.media = self.db.get_song_by_id(id=id)

    @authenticated
    @require_fields("name", "tracks")
    def on_post(self, req: Request, resp: Response):
        """Create a song.
        
        Requires authentication.
        """
        pk = self.db.create_song(
            name=req.media["name"], tracks=req.media["tracks"]
        )
        self.db.create_song_user_link(pk, req.username)
        resp.media = self.db.get_song_by_id(id=pk)
        resp.status = falcon.HTTP_201

    @authenticated
    def on_delete(self, req: Request, resp: Response, pk: str):
        """Delete a song.

        Requires authentication.
        """
        self.db.delete_song(id=parse_int(pk), username=req.username)
        resp.status = falcon.HTTP_204
