# Custom Falcon error handlers.
# See: https://falcon.readthedocs.io/en/stable/api/api.html#falcon.API.add_error_handler

import falcon

from .db import DoesNotExist


def on_does_not_exist(exc: DoesNotExist, *args):
    """Return a 404 error page when a database object was not found."""
    raise falcon.HTTPNotFound(title=exc.message)
