import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE playlist
             (SongId varchar(5) PRIMARY KEY
              )''')

conn.commit()

conn.close()