import datetime
import json
import os
import sqlite3
from contextlib import suppress
from typing import List, Optional


class DoesNotExist(Exception):
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

    def get_song_by_id(self, id: int) -> dict:
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

    def delete_song(self, id: int, username: str) -> bool:
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

    def user_exists(self, username) -> bool:
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
        with self:
            self.cursor.execute(
                """INSERT INTO users (UserName, FirstName, LastName, Password)
                            VALUES (?,?,?,?)""",
                (username, first_name, last_name, password),
            )
            self.connection.commit()

    def get_user(self, username: str) -> dict:
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
        with self:
            count = self.cursor.execute(
                """DELETE FROM tokens WHERE Token = ?""", (token,)
            ).rowcount
            if count == 0:
                raise DoesNotExist("Token", token=token)
            self.connection.commit()

    def check_user(self, username: str, password: str) -> bool:
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
