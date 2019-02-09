import datetime
import json
import sqlite3

vars = dict()

def create_database_table(database_path):
    print("Creating database ...")
    vars['conn'] = sqlite3.connect(database_path)
    vars['cursor'] = vars['conn'].cursor()

    vars['cursor'].execute('''CREATE TABLE IF NOT EXISTS songs
                      (SongID integer primary key not null,
                      SongName text,
                      Created datetime,
                      Updated datetime,
                      TracksJson text)''')
    vars['cursor'].execute('''CREATE TABLE IF NOT EXISTS users
                      (UserName text primary key not null,
                      FirstName text,
                      LastName text,
                      Password text)''')
    vars['cursor'].execute('''CREATE TABLE IF NOT EXISTS song_user_links
                      (LinkID integer primary key not null,
                      SongID integer references songs,
                      UserName text references users)''')
    vars['cursor'].execute('''CREATE TABLE IF NOT EXISTS tokens
                      (Token text primary key not null,
                      UserName text references users,
                      RefreshDate datetime)''')
    vars['conn'].commit()
    return True


def create_song(song_name, tracks_json):
    current_time = datetime.datetime.now()
    vars['cursor'].execute('''INSERT INTO songs (SongName, Created, Updated, TracksJson)
                      VALUES (?,?,?,?)''', (song_name, current_time, current_time, tracks_json))
    vars['conn'].commit()
    vars['cursor'].execute("SELECT SongID FROM songs WHERE Created = ? and SongName = ? ", (current_time, song_name))
    result = vars['cursor'].fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return None


def update_song(song_id, song_name, tracks_json):
    current_time = datetime.datetime.now()
    if song_id_exists(song_id):
        vars['cursor'].execute('''UPDATE songs
                          SET SongName = ?,
                              Updated = ?,
                              TracksJson = ?
                          WHERE SongID = ?''', (song_name, current_time, tracks_json, song_id))
        vars['conn'].commit()
        return get_song_by_id(song_id)
    else:
        return None


def delete_song(song_id):
    vars['cursor'].execute("SELECT SongID FROM songs WHERE SongID = ?", (song_id,))
    result = vars['cursor'].fetchall()
    if len(result) == 1:
        vars['cursor'].execute('''DELETE FROM songs WHERE SongID = ?''', (song_id,))
        vars['cursor'].execute('''DELETE FROM song_user_links WHERE SongID = ?''', (song_id,))
        vars['conn'].commit()
        return True
    else:
        return False


def create_user(user_name, first_name, last_name, password):
    if is_user_name_free(user_name):
        vars['cursor'].execute('''INSERT INTO users (UserName, FirstName, LastName, Password)
                          VALUES (?,?,?,?)''', (user_name, first_name, last_name, password))
        vars['conn'].commit()
        return True
    else:
        return False


def get_user_info(user_name):
    vars['cursor'].execute("SELECT UserName, FirstName, LastName FROM users WHERE UserName=?", [user_name])
    result = vars['cursor'].fetchone()
    if result is not None:
        output = {
            "username" : result[0],
            "first_name" : result[1],
            "last_name" : result[2],
           }
        return output
    return ""


def create_song_user_link(song_id, user_name):
    if song_id_exists(song_id) and not (is_user_name_free(user_name)):
        vars['cursor'].execute('''INSERT INTO song_user_links (SongID, UserName)
                          VALUES (?,?)''', (song_id, user_name))
        vars['conn'].commit()
        return True
    else:
        return False


def create_token(user_name, token):
    if not is_user_name_free(user_name) and is_token_valid(token) is None:
        vars['cursor'].execute('''INSERT INTO tokens (Token, UserName, RefreshDate)
                          VALUES (?,?,?)''',
                       (token, user_name, datetime.datetime.now() + datetime.timedelta(minutes=15)))
        vars['conn'].commit()
        return True
    else:
        return False


def delete_token(token):
    vars['cursor'].execute("SELECT Token FROM tokens WHERE Token = ?", [token])
    result = vars['cursor'].fetchall()
    if len(result) == 1:
        vars['cursor'].execute('''DELETE FROM tokens WHERE Token = ?''', [token])
        vars['conn'].commit()
        return True
    else:
        return False


def delete_obsolete_tokens():
    vars['cursor'].execute('''DELETE FROM tokens WHERE RefreshDate <=  ?''', datetime.datetime.now())
    vars['conn'].commit()
    return True


def get_song_by_id(song_id):
    if song_id_exists(song_id):
        vars['cursor'].execute("SELECT * FROM songs WHERE SongID = ? ", (song_id,))
        result = vars['cursor'].fetchone()
        return strings2dict(result[0], result[1], result[2], result[3], result[4])
    else:
        return None


def get_songs_by_user(user_name):
    """Return list of songs where the user is contributing
    user_name : string
        Name of user
    Returns
    -------------
        list of dictionaries
    """
    if not (is_user_name_free(user_name)):
        vars['cursor'].execute('''SELECT *
                          FROM songs, song_user_links
                          ON songs.SongID = song_user_links.SongID
                          WHERE UserName = ? ''', [user_name])
        result = vars['cursor'].fetchall()
        list_of_songs = []
        for song in result:
            list_of_songs.append(strings2dict(song[0], song[1], song[2], song[3], song[4]))
        return list_of_songs
    else:
        return None


def check_user(user_name, password):
    if is_user_name_free(user_name):
        return False
    else:
        vars['cursor'].execute("SELECT Password FROM users WHERE UserName=?", [user_name])
        if vars['cursor'].fetchone()[0] == password:
            return True
        else:
            return False


def song_id_exists(song_id):
    vars['cursor'].execute("SELECT count(SongID) FROM songs WHERE SongID=?", (song_id,))
    if vars['cursor'].fetchone()[0] == 1:
        return True
    else:
        return False


def is_user_name_free(user_name):
    vars['cursor'].execute("SELECT count(UserName) FROM users WHERE UserName=?", [user_name])
    if vars['cursor'].fetchone()[0] == 0:
        return True
    else:
        return False


def is_token_valid(token):
    vars['cursor'].execute("SELECT UserName FROM tokens WHERE Token=?", [token])
    result = vars['cursor'].fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return None


def check_user_token(user_name):
    vars['cursor'].execute("SELECT Token, RefreshDate FROM tokens WHERE UserName=?", [user_name])
    result = vars['cursor'].fetchall()
    if len(result) > 0:
        count = 0
        for token_date in result:
            if token_date[1] < datetime.datetime.now():
                count += 1
                sole_valid_token = token_date[0]
        if count == 1:
            return sole_valid_token
    else:
        return None


def strings2dict(song_id, song_name, created, updated, tracks):
    output = {}
    output['id'] = song_id
    output['name'] = song_name
    output['created'] = str(created)
    output['updated'] = str(updated)
    output['tracks'] = json.loads(tracks)
    return output


if __name__ == "__main__":
    # If database is empty, create tables
    create_database_table()
