import sqlite3

fname = 'Organized Bible Books.txt'
fhandle = open(fname)

conn = sqlite3.connect('MemScript_E.db')
cur = conn.cursor()

for line in fhandle:
    book_name = str(line).strip('\n')
    cur.execute("""
    CREATE TABLE '""" + book_name + """' (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `chap`	INTEGER NOT NULL,
    `ver`	INTEGER NOT NULL,
    `tex`	TEXT NOT NULL,
    `popularity`   INTEGER NOT NULL
)""")
    conn.commit()

