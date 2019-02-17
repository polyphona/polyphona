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
    """Create a new application instance.

    - For simplicity, CORS is enabled for all origins,
      all methods and all headers.
    - ``DoesNotExist`` exceptions are caught and converted
      to ``404 Not Found`` error responses.

    Parameters
    ----------
    db : Database
        An instance of the ``Database``.
    
    Returns
    -------
    api : API
    """
    # Middleware.
    cors = CORS(
        allow_all_origins=True, allow_all_methods=True, allow_all_headers=True
    )

    # Application instance.
    api = API(middleware=[cors.middleware])

    # Error handlers.
    api.add_error_handler(DoesNotExist, on_does_not_exist)

    # Resources.
    users = UserResource(db)
    user_songs = UserSongsResource(db)
    song = SongResource(db)
    token = TokenResource(db)

    # Routes.
    api.add_route("/users/", users)
    api.add_route("/users/{username}/songs", user_songs)
    api.add_route("/songs/{pk}", song)
    api.add_route("/songs/", song)
    api.add_route("/tokens/{token}", token)
    api.add_route("/tokens/", token)

    return api
