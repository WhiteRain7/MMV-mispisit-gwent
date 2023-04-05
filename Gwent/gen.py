import sqlite3 as sql
import random

def generate_name():
    first_names = ['John', 'Michael', 'Samantha', 'David', 'Sarah', 'William', 'Olivia', 'Daniel', 'Ava', 'James', 'Isabella', 'Benjamin', 'Mia', 'Jacob', 'Sophia', 'Ethan', 'Charlotte', 'Lucas', 'Amelia', 'Mason', 'Harper', 'Elijah', 'Evelyn', 'Logan', 'Abigail', 'Alexander', 'Emily', 'Sebastian', 'Elizabeth']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson']

    return f"{random.choice(first_names)} {random.choice(last_names)}"

base = sql.connect('gwent_db.sqlite3')

base.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL,
        email UNIQUE
    )
''')

base.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_1 INTEGER REFERENCES users (id) NOT NULL,
        player_2 INTEGER REFERENCES users (id) NOT NULL,
        result INTEGER DEFAULT -1 CHECK(result IN (-1, 0, 1, 2)),
        deck_1 TEXT,
        deck_2 TEXT,
        actions TEXT
    )
''')

base.executemany('INSERT INTO users (nickname, email) VALUES (?, ?)', [
    ((name:= generate_name()), 
     name.replace(' ', '_') + 
     '_' +
     str(random.randint(1, 999)) +
     '@email.' + random.choice(['ru', 'en', 'fr', 'com'])) for _ in range(random.randint(3,10))
])

base.commit()
base.close()