import sqlite3

db_created = True

conn = sqlite3.connect('database.db')
cur = conn.cursor()

if not db_created:
    cur.execute('''CREATE TABLE store
        (id text, album text, artist text, price integer)''')
    cur.execute("INSERT INTO store VALUES ('11453', 'Hotel California', 'Eagles', 150)")

cur.execute('SELECT * FROM store')
s = cur.fetchone()
print(s)

# commit and close
# conn.commit()
conn.close()
