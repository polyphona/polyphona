from functools import wraps

import falcon


def authenticated(responder):
    """Require the client to provide a valid token to access the endpoint."""

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


def require_fields(*fields: str):
    def decorate(responder):
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
