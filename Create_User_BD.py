import sqlite3 as sql
with sql.connect("users.db") as udb:
    cur = udb.cursor()
    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE, city TEXT NOT NULL)")
    cur.execute("CREATE TABLE vieved(user_id INT, movie_id VARCHAR, movie_name VARCHAR)")