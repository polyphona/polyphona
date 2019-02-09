from uuid import uuid4

import falcon
from falcon import Request, Response

from ..db import Database
from .decorators import require_fields


class TokenResource:
    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "password")
    def on_post(self, req: Request, resp: Response):
        data = req.media

        if not self.db.check_user(data["username"], data["password"]):
            raise falcon.HTTPUnauthorized("Invalid credentials.")

        # Try and generate a new token
        new_token = str(uuid4())
        if self.db.is_token_valid(new_token) is not None:
            new_token = str(uuid4())
        if self.db.is_token_valid(new_token) is not None:
            raise falcon.HTTPLoopDetected("Cannot generate token.")
        if not self.db.create_token(data["username"], new_token):
            raise falcon.HTTPError(
                falcon.HTTP_500, "Failed to validate token (unexcepted)."
            )

        resp.media = {
            "token": new_token,
            "user": self.db.get_user_info(data["username"]),
        }

    def on_delete(self, _, resp: Response, token: str):
        if not self.db.delete_token(token):
            raise falcon.HTTPNotFound(title="Token does not exist.")
        resp.status = falcon.HTTP_204
