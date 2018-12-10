import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()

    #If database is empty, create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs 
                      (SongID integer primary key not null,
                      Json text,
                      User text)''')
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

def addUser():
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()

def getSongByTitle():
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()

def songsByUser():
    conn = sqlite3.connect('polyphona_db.db')
    cursor = conn.cursor()


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