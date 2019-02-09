import os
import datetime
import json
import sqlite3
from contextlib import suppress
from typing import List, Optional


class Database:
    def __init__(self, path: str):
        self.path = path
        self.connections: List[sqlite3.Connection] = []
        self.cursors: List[sqlite3.Cursor] = []

    def __enter__(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        self.connections.append(conn)
        self.cursors.append(cursor)
        return self

    def __exit__(self, *args):
        with suppress(IndexError):
            self.cursors.pop().close()

        with suppress(IndexError):
            self.connections.pop().close()

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.cursors[-1]

    @property
    def connection(self) -> sqlite3.Connection:
        return self.connections[-1]

    def generate_schema(self):
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
        os.remove(self.path)

    def song_id_exists(self, id: int) -> bool:
        with self:
            self.cursor.execute(
                "SELECT count(SongID) FROM songs WHERE SongID = ?", (id,)
            )
            return self.cursor.fetchone()[0] == 1

    def get_song_by_id(self, id: int) -> dict:
        with self:
            if not self.song_id_exists(id):
                return None

            self.cursor.execute("SELECT * FROM songs WHERE SongID = ? ", (id,))
            result = self.cursor.fetchone()
            return strings2dict(
                result[0], result[1], result[2], result[3], result[4]
            )

    def get_songs_by_user(self, username: str) -> List[dict]:
        """Return list of songs where the user is contributing
        user_name : string
            Name of user
        Returns
        -------------
            list of dictionaries
        """
        with self:
            if not self.user_exists(username):
                self.cursor.execute(
                    """
                    SELECT *
                    FROM songs, song_user_links
                    ON songs.SongID = song_user_links.SongID
                    WHERE UserName = ?
                    """,
                    (username,),
                )
                result = self.cursor.fetchall()
                list_of_songs = []
                for song in result:
                    list_of_songs.append(
                        strings2dict(
                            song[0], song[1], song[2], song[3], song[4]
                        )
                    )
                return list_of_songs
            return []

    def create_song(self, name: str, tracks: List[dict]) -> int:
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
            row_id = self.cursor.fetchall()[0][0]
            return row_id

    def update_song(self, id: int, name: str, tracks: List[dict]) -> dict:
        with self:
            if not self.song_id_exists(id):
                return None

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

    def delete_song(self, id: int) -> bool:
        with self:
            self.cursor.execute(
                "SELECT SongID FROM songs WHERE SongID = ?", (id,)
            )
            result = self.cursor.fetchall()
            if len(result) == 1:
                self.cursor.execute("DELETE FROM songs WHERE SongID = ?", (id,))
                self.cursor.execute(
                    "DELETE FROM song_user_links WHERE SongID = ?", (id,)
                )
                self.connection.commit()
                return True
            return False

    def create_user(
        self, username: str, first_name: str, last_name: str, password: str
    ):
        with self:
            self.cursor.execute(
                """INSERT INTO users (UserName, FirstName, LastName, Password)
                            VALUES (?,?,?,?)""",
                (username, first_name, last_name, password),
            )
            self.connection.commit()

    def user_exists(self, username) -> bool:
        with self:
            self.cursor.execute(
                "SELECT count(UserName) FROM users WHERE UserName=?",
                (username,),
            )
            return self.cursor.fetchone()[0] == 0

    def get_user_info(self, username: str) -> dict:
        with self:
            self.cursor.execute(
                "SELECT UserName, FirstName, LastName FROM users WHERE UserName=?",
                (username,),
            )
            result = self.cursor.fetchone()
            if result is not None:
                output = {
                    "username": result[0],
                    "first_name": result[1],
                    "last_name": result[2],
                }
                return output
            return {}

    def is_token_valid(self, token: str) -> Optional[str]:
        with self:
            self.cursor.execute(
                "SELECT UserName FROM tokens WHERE Token=?", (token,)
            )
            result = self.cursor.fetchall()
            if len(result) == 1:
                return result[0][0]
            return None

    def create_song_user_link(self, song_id: int, username: str) -> bool:
        with self:
            if self.song_id_exists(song_id) and not (
                self.user_exists(username)
            ):
                self.cursor.execute(
                    """
                    INSERT INTO song_user_links (SongID, UserName)
                    VALUES (?,?)
                    """,
                    (song_id, username),
                )
                self.connection.commit()
                return True
            return False

    # TODO: rename to `save_token()`
    def create_token(self, username: str, token: str) -> bool:
        with self:
            if not self.user_exists(username) and not self.is_token_valid(
                token
            ):
                refresh = datetime.datetime.now() + datetime.timedelta(
                    minutes=15
                )
                self.cursor.execute(
                    """
                    INSERT INTO tokens (Token, UserName, RefreshDate)
                    VALUES (?,?,?)
                    """,
                    (token, username, refresh),
                )
                self.connection.commit()
                return True
            return False

    def delete_token(self, token: str) -> bool:
        with self:
            self.cursor.execute(
                "SELECT Token FROM tokens WHERE Token = ?", (token,)
            )
            result = self.cursor.fetchall()
            if len(result) == 1:
                self.cursor.execute(
                    """DELETE FROM tokens WHERE Token = ?""", (token,)
                )
                self.connection.commit()
                return True
            return False

    def delete_obsolete_tokens(self) -> bool:
        with self:
            self.cursor.execute(
                "DELETE FROM tokens WHERE RefreshDate <= ?",
                datetime.datetime.now(),
            )
            self.connection.commit()
            return True

    def check_user(self, username: str, password: str):
        with self:
            if self.user_exists(username):
                return False
            self.cursor.execute(
                "SELECT Password FROM users WHERE UserName=?", (username,)
            )
            if self.cursor.fetchone()[0] == password:
                return True
            return False

    def check_user_token(self, username: str) -> Optional[str]:
        with self:
            self.cursor.execute(
                "SELECT Token, RefreshDate FROM tokens WHERE UserName=?",
                (username,),
            )
            result = self.cursor.fetchall()
            if len(result) > 0:
                count = 0
                for token_date in result:
                    if token_date[1] < datetime.datetime.now():
                        count += 1
                        sole_valid_token = token_date[0]
                if count == 1:
                    return sole_valid_token
            return None


def strings2dict(song_id, song_name, created, updated, tracks):
    output = {}
    output["id"] = song_id
    output["name"] = song_name
    output["created"] = str(created)
    output["updated"] = str(updated)
    output["tracks"] = json.loads(tracks)
    return output
