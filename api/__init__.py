import os

from .server import create_api
from .db import Database

# WSGI application.
db = Database(os.environ.get("DATABASE", "polyphona.db"))
app = create_api(db)
