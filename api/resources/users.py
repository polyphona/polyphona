import falcon
from falcon import Request, Response


from ..db import Database
from .decorators import require_fields


class UserResource:
    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "first_name", "last_name", "password")
    def on_post(self, req: Request, resp: Response):
        data: dict = req.media

        if not self.db.is_user_name_free(data["username"]):
            raise falcon.HTTPBadRequest("Username already taken.")

        if not self.db.create_user(
            data["username"],
            data["first_name"],
            data["last_name"],
            data["password"],
        ):
            raise falcon.HTTPError(falcon.HTTP_500, "Unexpected server error.")

        resp.status = falcon.HTTP_201
