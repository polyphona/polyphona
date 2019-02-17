import os

from .db import Database
from .factory import create_api

# WSGI application.
db = Database(os.environ.get("DATABASE", "polyphona.db"))
app = create_api(db)
