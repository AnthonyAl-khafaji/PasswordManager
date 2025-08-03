import sqlite3

class userDB:
    def __init__(self, dbPath: str = 'users.db'):
        self.dbPath = dbPath
        self.createUserTable()  # Ensure the table is created on initialization

    def connect(self):
        return sqlite3.connect(self.dbPath)

    def createUserTable(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    passwordHash BLOB NOT NULL
                )
            """)
            conn.commit()

    def AddUser(self, username: str, passwordHash: str):
        try:
            with self.connect() as conn:
                conn.execute(
                    "INSERT INTO users (username, passwordHash) VALUES (?, ?)",
                    (username, passwordHash)
                )
                conn.commit() 
            return True
        except sqlite3.IntegrityError:
            return False

    def GetPassHash(self, username: str):
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT passwordHash FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return row[0]
        
    def userExists(self, username: str):
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone() is not None

                




