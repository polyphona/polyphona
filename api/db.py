import datetime
import json
import os
import sqlite3
from contextlib import suppress
from typing import List, Optional


class DoesNotExist(Exception):
    """Raised when an object could not be found is the database.

    Parameters
    ----------
    obj_type : str
        A label that indicates what type the object should have been.
    **kwargs : dict of str to str
        Attribute names and values that the object should have had.
    """

    def __init__(self, obj_type: str, **kwargs: str):
        if kwargs:
            attrs = " with " + ", ".join(
                [f"{key}={value}" for key, value in kwargs.items()]
            )
        else:
            attrs = ""
        self.message = f"{obj_type}{attrs} does not exist."
        super().__init__(self.message)


class Database:
    """The single entry point to the database.

    This class exposes methods to interact with the database and manages
    connections and cursors itself.

    Parameters
    ----------
    path : str
        The path to the SQLite database file (that exists or should be created).
    """

    def __init__(self, path: str):
        self.path = path
        self._connections: List[sqlite3.Connection] = []
        self._cursors: List[sqlite3.Cursor] = []

    # Context manager implementation.
    # Allows to use `with self:` to acquire a new connection/cursor.
    # The connections and cursors are stored in a stack-like manner, so it
    # is safe to enter the database context multiple times
    # (i.e. perform nested queries.)

    def __enter__(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        self._connections.append(conn)
        self._cursors.append(cursor)
        return self

    def __exit__(self, *args):
        with suppress(IndexError):
            self._cursors.pop().close()

        with suppress(IndexError):
            self._connections.pop().close()

    @property
    def cursor(self) -> sqlite3.Cursor:
        """Returns the current cursor.

        Note: a cursor can only be available when inside the context
        of the database.
    
        Returns
        -------
        cursor : sqlite3.Cursor

        Raises
        ------
        IndexError :
            If no cursor is available.
        """
        return self._cursors[-1]

    @property
    def connection(self) -> sqlite3.Connection:
        """Returns the current database connection.

        Note: a connection can only be available when inside the context
        of the database.

        Returns
        -------
        connection : sqlite3.Connection

        Raises
        ------
        IndexError :
            If no connection is available.
        """
        return self._connections[-1]

    def generate_schema(self):
        """Generate the database schema.

        It is safe to call this multiple times: tables will only be
        created if they don't exist already.
        """
        with self:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS songs (
                    SongID integer primary key not null,
                    SongName text,
                    Created datetime,
                    Updated datetime,
                    TracksJson text
                )"""
            )
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    UserName text primary key not null,
                    FirstName text,
                    LastName text,
                    Password text
                )"""
            )
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS song_user_links (
                    LinkID integer primary key not null,
                    SongID integer references songs,
                    UserName text references users
                )"""
            )
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS tokens (
                    Token text primary key not null,
                    UserName text references users,
                    RefreshDate datetime
                )"""
            )
            self.connection.commit()

    def remove(self):
        """Delete the SQLite database file."""
        os.remove(self.path)

    def get_song_by_id(self, id: int) -> dict:
        """Retrieve a song by ID.

        Parameters
        ----------
        id : int
            The ID of the song.
        
        Returns
        -------
        song : dict
        """
        with self:
            self.cursor.execute(
                """
                SELECT SongID, SongName, Created, Updated, TracksJson
                FROM songs
                WHERE SongID = ?
                """,
                (id,),
            )
            try:
                id, name, created, updated, tracks = self.cursor.fetchone()
            except TypeError:
                raise DoesNotExist("Song", id=id)
            else:
                return {
                    "id": id,
                    "name": name,
                    "created": str(created),
                    "updated": str(updated),
                    "tracks": json.loads(tracks),
                }

    def get_songs_by_user(self, username: str) -> List[dict]:
        """Return the list of songs for a given user.

        Parameters
        ----------
        username : str

        Returns
        -------
        songs : list of dict
        """
        with self:
            self.cursor.execute(
                """
                SELECT songs.SongID, SongName, Created, Updated, TracksJson
                FROM songs, song_user_links
                ON songs.SongID = song_user_links.SongID
                WHERE UserName = ?
                """,
                (username,),
            )
            result = self.cursor.fetchall()
            return [strings2dict(*song) for song in result]

    def create_song(self, name: str, tracks: List[dict]) -> int:
        """Save a new song to the database.

        Parameters
        ----------
        name : str
            The name of the song.
        tracks : list of dict
            A list of JSON-serializable dictionaries.

        Returns
        -------
        song_id : int
            The ID of the song newly created. The full data can be fetched
            using ``.get_song_by_id()``.
        """
        with self:
            now = datetime.datetime.now()
            self.cursor.execute(
                """
                INSERT INTO songs (SongName, Created, Updated, TracksJson)
                VALUES (?,?,?,?)
                """,
                (name, now, now, json.dumps(tracks)),
            )
            self.connection.commit()
            self.cursor.execute(
                "SELECT SongID FROM songs WHERE Created = ? AND SongName = ?",
                (now, name),
            )
            row_id: int = self.cursor.fetchall()[0][0]
            return row_id

    def update_song(
        self, id: int, name: str, tracks: List[dict], username: str
    ) -> dict:
        """Update a song.

        Parameters
        ----------
        id : int
            The ID of the song to update.
        name : str
            The new name for this song.
        tracks : list of dict
            The new list of tracks for this song.
        username : str
            The user this song belongs to.
        
        Returns
        -------
        song : dict
        """
        with self:
            self.cursor.execute(
                """
                SELECT songs.SongID
                FROM songs, song_user_links
                ON songs.SongID = song_user_links.SongID
                WHERE songs.SongID = ?
                AND song_user_links.UserName = ? 
                """,
                (id, username),
            )
            if self.cursor.fetchone() is None:
                raise DoesNotExist("Song", id=id, username=username)

            now = datetime.datetime.now()
            self.cursor.execute(
                """
                UPDATE songs
                SET SongName = ?, Updated = ?, TracksJson = ?
                WHERE SongID = ?
                """,
                (name, now, json.dumps(tracks), id),
            )
            self.connection.commit()
            return self.get_song_by_id(id)

    def delete_song(self, id: int, username: str):
        """Delete a song.

        Parameters
        ----------
        id : int
            The ID of the song to delete.
        username : str
            The user the song belongs to.
        
        Raises
        ------
        DoesNotExist :
            If no song exists for ``id`` and ``username``.
        """
        with self:
            self.cursor.execute(
                """
                SELECT songs.SongID
                FROM songs, song_user_links
                ON songs.SongID = song_user_links.SongID
                WHERE songs.SongID = ?
                AND song_user_links.UserName = ? 
                """,
                (id, username),
            )
            if self.cursor.fetchone() is None:
                raise DoesNotExist("Song", id=id, username=username)

            self.cursor.execute("DELETE FROM songs WHERE SongID = ?", (id,))
            self.cursor.execute(
                "DELETE FROM song_user_links WHERE SongID = ?", (id,)
            )
            self.connection.commit()

    def user_exists(self, username: str) -> bool:
        """Return whether a user already exists in the database.

        Parameters
        ----------
        username : str

        Returns
        -------
        exists : bool
        """
        with self:
            self.cursor.execute(
                "SELECT count(UserName) FROM users WHERE UserName=?",
                (username,),
            )
            count, = self.cursor.fetchone()
            return count == 0

    def create_user(
        self, username: str, first_name: str, last_name: str, password: str
    ):
        """Save a new user to the database.

        Parameters
        ----------
        username : str
        first_name : str
        last_name : str
        password: str
        """
        with self:
            self.cursor.execute(
                """INSERT INTO users (UserName, FirstName, LastName, Password)
                            VALUES (?,?,?,?)""",
                (username, first_name, last_name, password),
            )
            self.connection.commit()

    def get_user(self, username: str) -> dict:
        """Retrieve an user.

        Parameters
        ----------
        username : str

        Returns
        -------
        user : dict
        """
        with self:
            self.cursor.execute(
                """
                SELECT UserName, FirstName, LastName
                FROM users
                WHERE UserName=?
                """,
                (username,),
            )
            username, first_name, last_name = self.cursor.fetchone()
            return {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }

    def create_song_user_link(self, song_id: int, username: str):
        """Attach a song to an user.

        Parameters
        ----------
        song_id : int
        username : str
        """
        with self:
            self.cursor.execute(
                """
                INSERT INTO song_user_links (SongID, UserName)
                VALUES (?,?)
                """,
                (song_id, username),
            )
            self.connection.commit()

    def save_token(self, username: str, token: str):
        """Save a new token to the database.

        The token's refresh date will be set to 15mins ahead from now.

        Parameters
        ----------
        username : str
        token : str
        """
        with self:
            refresh = datetime.datetime.now() + datetime.timedelta(minutes=15)
            self.cursor.execute(
                """
                INSERT INTO tokens (Token, UserName, RefreshDate)
                VALUES (?,?,?)
                """,
                (token, username, refresh),
            )
            self.connection.commit()

    def reverse_token(self, token: str) -> Optional[str]:
        """Retrieve the username corresponding to a token, if any.

        Parameters
        ----------
        token : str

        Returns
        -------
        username : str or None
            This is ``None`` if ``token`` does not correspond to any user.
        """
        with self:
            self.cursor.execute(
                "SELECT UserName FROM tokens WHERE Token=?", (token,)
            )
            result = self.cursor.fetchall()
            try:
                username = result[0][0]
                return username
            except IndexError:
                return None

    def delete_token(self, token: str):
        """Delete a token from the database.

        Parameters
        ----------
        token : str

        Raises
        ------
        DoesNotExist :
            If no token identified by ``token`` exists.
        """
        with self:
            count = self.cursor.execute(
                """DELETE FROM tokens WHERE Token = ?""", (token,)
            ).rowcount
            if count == 0:
                raise DoesNotExist("Token", token=token)
            self.connection.commit()

    def check_user(self, username: str, password: str) -> bool:
        """Check that the given credentials match those stored in database.

        Parameters
        ----------
        username : str
        password : str

        Returns
        -------
        correct : bool
        """
        if self.user_exists(username):
            return False

        with self:
            self.cursor.execute(
                "SELECT Password FROM users WHERE UserName=?", (username,)
            )
            return self.cursor.fetchone()[0] == password


def strings2dict(song_id, song_name, created, updated, tracks):
    output = {}
    output["id"] = song_id
    output["name"] = song_name
    output["created"] = str(created)
    output["updated"] = str(updated)
    output["tracks"] = json.loads(tracks)
    return output
