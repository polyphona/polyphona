from uuid import uuid4

import falcon
from falcon import Request, Response

from ..db import Database
from .decorators import require_fields


class TokenResource:
    """Resource to create or delete tokens."""

    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "password")
    def on_post(self, req: Request, resp: Response):
        """Exchange user credentials for a new token.
        
        The payload must contain the ``username`` and ``password`` fields.
        
        Raises
        ------
        falcon.HTTPUnauthorized
            If the given credentials are invalid.
        """

        username = req.media["username"]
        password = req.media["password"]

        if not self.db.check_user(username, password):
            raise falcon.HTTPUnauthorized("Invalid credentials.")

        token = str(uuid4())
        self.db.save_token(username, token)

        resp.media = {"token": token, "user": self.db.get_user(username)}

    def on_delete(self, _, resp: Response, token: str):
        """Delete a token."""
        self.db.delete_token(token)
        resp.status = falcon.HTTP_204
