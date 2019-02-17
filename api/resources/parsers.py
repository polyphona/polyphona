import falcon


def parse_int(value: str) -> int:
    """Parse an inbound string value into an integer.

    This is meant to be used in the context of a Falcon responder, so that
    an invalid string triggers a ``400 Bad Request`` error response.

    Parameters
    ----------
    value : str

    Returns
    -------
    as_int : int

    Raises
    ------
    HTTPBadRequest :
        If ``value`` could not be converted to an integer.
    """
    try:
        return int(value)
    except TypeError:
        raise falcon.HTTPBadRequest(f"Cannot interpret {value} as an integer")
