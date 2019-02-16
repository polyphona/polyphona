"""API factory."""

# API specification: https://hackmd.io/eNiNVR6eR1mJH2kOebtE5g#

from falcon import API
from falcon_cors import CORS

from .db import Database, DoesNotExist
from .resources.songs import UserSongsResource, SongResource
from .resources.tokens import TokenResource
from .resources.users import UserResource
from .error_handlers import on_does_not_exist


def create_api(db: Database) -> API:
    cors = CORS(
        allow_all_origins=True, allow_all_methods=True, allow_all_headers=True
    )
    api = API(middleware=[cors.middleware])

    api.add_error_handler(DoesNotExist, on_does_not_exist)

    api.add_route("/users/", UserResource(db))

    api.add_route("/users/{username}/songs", UserSongsResource(db))

    song_resource = SongResource(db)
    api.add_route("/songs/{pk}", song_resource)
    api.add_route("/songs/", song_resource)

    token_resource = TokenResource(db)
    api.add_route("/tokens/{token}", TokenResource(db))
    api.add_route("/tokens/", token_resource)

    return api
