import falcon
from falcon import Request, Response


from ..db import Database
from .decorators import require_fields


class UserResource:
    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "first_name", "last_name", "password")
    def on_post(self, req: Request, resp: Response):
        json_in: dict = req.media

        if not self.db.is_user_name_free(json_in["username"]):
            raise falcon.HTTPBadRequest("Username already taken.")

        if not self.db.create_user(
            json_in["username"],
            json_in["first_name"],
            json_in["last_name"],
            json_in["password"],
        ):
            raise falcon.HTTPError(falcon.HTTP_500, "Unexpected server error.")

        resp.status = falcon.HTTP_201
