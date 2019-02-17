import falcon
from falcon import Request, Response


from ..db import Database
from .decorators import require_fields


class UserResource:
    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "first_name", "last_name", "password")
    def on_post(self, req: Request, resp: Response):
        username = req.media["username"]

        if not self.db.user_exists(username):
            raise falcon.HTTPBadRequest(f"User {username} already exists.")

        self.db.create_user(**req.media)

        resp.status = falcon.HTTP_201
