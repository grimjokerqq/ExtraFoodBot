import sqlite3 as sq

base = sq.connect('Dostavka.db')

cursor = base.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tagam_turleri(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tagamdar(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_id INTEGER,
                name TEXT,
                desc TEXT,
                price INTEGER,
                photo TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS sebet(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tagam_id INTEGER , FOREIGN KEY(id) REFERENCES tagamdar(id))''')

base.commit()