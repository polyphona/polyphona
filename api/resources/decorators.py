from functools import wraps
from typing import Callable

import falcon


def authenticated(responder: Callable) -> Callable:
    """Require the client to provide a valid token to access the endpoint.

    The token should be given in the ``Authorization`` header in the following
    format: ``Token {token}``.

    If the token was not given or it is invalid, a ``401 Unauthorized`` error
    response is sent.
    """

    @wraps(responder)
    def with_auth(self, req, resp, *args, **kwargs):
        _, _, token = (req.auth or "").partition("Token ")

        if not token:
            raise falcon.HTTPUnauthorized(
                "Authentication credentials were not provided."
            )

        username = self.db.reverse_token(token)
        if username is None:
            raise falcon.HTTPUnauthorized("Invalid token.")

        req.username = username
        return responder(self, req, resp, *args, **kwargs)

    return with_auth


def require_fields(*fields: str) -> Callable:
    """Require the client to provide the specified fields.

    This is meant to be used as a decorator of responder methods.

    Parameters
    ----------
    *fields : str
        Fields that the inbound JSON *must* contain. If it doesn't,
        A ``400 Bad Request`` response is returned.
    """

    def decorate(responder: Callable) -> Callable:
        @wraps(responder)
        def with_fields_required(self, req, resp, *args, **kwargs):
            for field in fields:
                if field not in req.media:
                    raise falcon.HTTPBadRequest(
                        f"'{field}': this field is required.."
                    )
            responder(self, req, resp, *args, **kwargs)

        return with_fields_required

    return decorate
