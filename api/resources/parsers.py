import falcon


def parse_int(value: str) -> int:
    """Parse an inbound string value into an integer."""
    try:
        return int(value)
    except TypeError:
        raise falcon.HTTPBadRequest(f"Cannot interpret {value} as an integer")
