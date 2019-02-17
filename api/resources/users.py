import falcon
from falcon import Request, Response


from ..db import Database
from .decorators import require_fields


class UserResource:
    """Resource to create users.

    Parameters
    -----------
    db : Database
    """

    def __init__(self, db: Database):
        self.db = db

    @require_fields("username", "first_name", "last_name", "password")
    def on_post(self, req: Request, resp: Response):
        """Create a new user.

        Required fields:

        - ``username``
        - ``first_name``
        - ``last_name``
        - ``password``
    
        Raises
        ------
        HTTPBadRequest :
            If a user named ``username`` already exists.
        """
        username = req.media["username"]

        if not self.db.user_exists(username):
            raise falcon.HTTPBadRequest(f"User {username} already exists.")

        self.db.create_user(**req.media)

        resp.status = falcon.HTTP_201
