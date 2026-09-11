import sqlite3

def init_db():
# Creates or opens the file database.db in the current dir
connection = sqlite3.connect('database.db')

# We create a cursor for executing SQL queries
cursor = connection.cursor()

# We create a table for posts if it does not exsist yet
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# We add one test entry so the db ins't empy 
cursor.execute('''
    INSERT INTO posts (author, content)
    VALUES ('System Admin', 'Witaj w bazie danych SQLite!')
''')

# We confirm the changes and close the connection
connection.commit()
connection.close()

print("The database has been successfully initialized!")

if __name__ == '__main__':
    init_db()
