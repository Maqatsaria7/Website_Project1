import sqlite3

conn = sqlite3.connect('fitnessproject.db')
c = conn.cursor()

conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                question TEXT NOT NULL
            )
        ''')
conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT NOT NULL,
                information TEXT NOT NULL
            )
''')
conn.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
''')

conn.execute('''
        ALTER TABLE posts ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
''')
conn.commit()
conn.close()