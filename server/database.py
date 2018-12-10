import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()

    #If database is empty, create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs 
                      (SongID integer primary key not null,
                      SongName text,
                      Created datetime,
                      Updated datetime,
                      TracksJson text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (UserName text primary key not null,
                      Password text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS song_user_links
                      (LinkID integer primary key not null,
                      SongID integer,
                      UserName text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tokens
                      (Token text primary key not null,
                      UserID text,
                      RefreshDate datetime)''')
    conn.commit()
    conn.close()



def addSong(Json_song, userName):
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (Json, User) VALUES (?,?)", ( Json_song, userName ))

def addUser(username, password):  #Backend has to check if the username doesn't exist
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (UserName, Password) VALUES (?,?)", ( username, password ))

def getSongByID(song_ID):
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs WHERE SongID = ? ", ( song_ID ))
    return cursor.fetchone()

def getSongsByUser(userName):
    """ Return list of songs where the user is contributing 
    userName : string
        Name of user
    Returns
    -------------
        list of songs
    """
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT *
                      FROM songs, song_user_links
                      ON songs.SongID = song_user_links.SongID
                      WHERE UserName = ? ''', ( userName ))
    return cursor.fetchall()


def connectUser(userName,password):
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count(UserName) FROM users WHERE UserName=?",userName)
    if cursor.fetchone()[0] == 0:
        print(1)
        #throw exception username doesn't exist
    else :
        cursor.execute("SELECT Password FROM users WHERE UserName=?",userName)
        if cursor.fetchone()[0] == password:
            return True
        else :
            return False