# server.py
# use : gunicorn server:app
# api : https://hackmd.io/eNiNVR6eR1mJH2kOebtE5g#
#

import json
from uuid import uuid4
from functools import wraps

from falcon import (
    API,
    HTTPError,
    HTTP_201,
    HTTP_204,
    HTTP_400,
    HTTP_401,
    HTTP_404,
    HTTP_500,
    HTTP_508,
    Request,
    Response,
)
from falcon_cors import CORS

from .db import Database


def validate_int(value: str) -> int:
    rtn = 0
    try:
        rtn = int(value)
    except:
        raise HTTPError(HTTP_400, "Invalid song ID.")
    return rtn


def authenticated(responder):
    """Require the client to provide a valid token to access the endpoint."""

    @wraps(responder)
    def with_auth(self, req, resp, *args, **kwargs):
        _, _, token = (req.auth or "").partition("Token ")

        if not token:
            raise HTTPError(
                HTTP_401, "Authentication credentials were not provided."
            )

        username = self.db.is_token_valid(token)
        if username is None:
            raise HTTPError(HTTP_401, "Invalid token.")

        req.username = username
        return responder(self, req, resp, *args, **kwargs)

    return with_auth


class UserResource:
    def __init__(self, db: Database):
        self.db = db

    def on_post(self, req: Request, resp: Response):
        json_in: dict = req.media

        # Check validity of request
        for field in "username", "first_name", "last_name", "password":
            if field not in json_in:
                raise HTTPError(HTTP_400, "Missing {} field.".format(field))

        if not self.db.is_user_name_free(json_in["username"]):
            raise HTTPError(HTTP_400, "Username already taken.")
        if not self.db.create_user(
            json_in["username"],
            json_in["first_name"],
            json_in["last_name"],
            json_in["password"],
        ):
            raise HTTPError(HTTP_500, "Unexpected server error.")

        resp.status = HTTP_201


class GetSongListResource:
    def __init__(self, db: Database):
        self.db = db

    def on_get(self, req: Request, resp: Response, username: str):
        if self.db.is_user_name_free(username):
            raise HTTPError(HTTP_404, "Username unknown.")

        # Generate response
        json_resp = self.db.get_songs_by_user(username)
        resp.body = json.dumps(json_resp)


class SongResource:
    def __init__(self, db: Database):
        self.db = db

    @authenticated
    def on_get(self, req: Request, resp: ResourceWarning, song_id_str: str):
        song_id = validate_int(song_id_str)

        song = self.db.get_song_by_id(song_id)
        if song is None:
            raise HTTPError(HTTP_404, "song_id unknown.")

        resp.media = song

    @authenticated
    def on_put(self, req: Request, resp: Response, song_id_str):
        song_id = validate_int(song_id_str)
        username = req.username
        songs = self.db.get_songs_by_user(username)
        song_id_list = [song["id"] for song in songs]
        if song_id not in song_id_list:
            raise HTTPError(HTTP_404, "Song ID unknown.")

        json_in = req.media
        for field in "name", "tracks":
            if field not in json_in.keys():
                raise HTTPError(HTTP_400, "Missing {} field.".format(field))

        # Process request
        self.db.update_song(
            song_id, json_in["name"], json.dumps(json_in["tracks"])
        )

    @authenticated
    def on_post(self, req: Request, resp: Response):
        json_in = req.media
        if "name" not in json_in.keys():
            raise HTTPError(HTTP_400, "Missing name field.")
        if "tracks" not in json_in.keys():
            raise HTTPError(HTTP_400, "Missing tracks field.")

        # Process request
        song_id = self.db.create_song(
            json_in["name"], json.dumps(json_in["tracks"])
        )
        self.db.create_song_user_link(song_id, req.username)
        resp.status = HTTP_201

    @authenticated
    def on_delete(self, req: Request, resp: Response, song_id_str):
        song_id = validate_int(song_id_str)

        songs = self.db.get_songs_by_user(req.username)
        song_id_list = []
        for song in songs:
            song_id_list.append(song["id"])
        if song_id not in song_id_list:
            # Song ID does not belong to user
            raise HTTPError(HTTP_404, "Song ID unknown.")

        # Process request
        self.db.delete_song(song_id)
        resp.status = HTTP_204


class TokenResource:
    def __init__(self, db: Database):
        self.db = db

    def on_post(self, req: Request, resp: Response):
        json_in = req.media

        # Check validity of request
        if "username" not in json_in.keys():
            raise HTTPError(HTTP_400, "Missing username field.")
        if "password" not in json_in.keys():
            raise HTTPError(HTTP_400, "Missing password field.")
        if not self.db.check_user(json_in["username"], json_in["password"]):
            raise HTTPError(HTTP_400, "Invalid login information.")

        # Try and generate a new token
        new_token = str(uuid4())
        if self.db.is_token_valid(new_token) is not None:
            new_token = str(uuid4())
        if self.db.is_token_valid(new_token) is not None:
            raise HTTPError(HTTP_508, "Cannot generate token.")
        if not self.db.create_token(json_in["username"], new_token):
            raise HTTPError(HTTP_500, "Failed to validate token (unexcepted).")

        # Generate response
        json_out = {
            "token": new_token,
            "user": self.db.get_user_info(json_in["username"]),
        }
        resp.body = json.dumps(json_out, ensure_ascii=False)

    def on_delete(self, _, resp: Response, token: str):
        if not self.db.delete_token(token):
            raise HTTPError(HTTP_404, "Invalid token.")
        resp.status = HTTP_204


def create_api(db: Database) -> API:
    cors = CORS(
        allow_all_origins=True, allow_all_methods=True, allow_all_headers=True
    )
    api = API(middleware=[cors.middleware])

    user_resource = UserResource(db)
    api.add_route("/users/", user_resource)

    get_song_list = GetSongListResource(db)
    api.add_route("/users/{username}/songs", get_song_list)

    update_delete_song = SongResource(db)
    api.add_route("/songs/{song_id_str}", update_delete_song)
    api.add_route("/songs/", update_delete_song)

    token_resource = TokenResource(db)
    api.add_route("/tokens/{token}", token_resource)
    api.add_route("/tokens/", token_resource)

    return api
