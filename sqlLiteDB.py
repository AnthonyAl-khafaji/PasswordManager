import sqlite3

class userDB:
    def __init__(self, dbPath: str = 'users.db'):
        self.dbPath = dbPath
        #self.createUserTable()  

    def connect(self):
        return sqlite3.connect(self.dbPath)

    def siteTable(self):
        sql = """CREATE TABLE IF NOT EXISTS sites (  
                 siteID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 siteURL TEXT NOT NULL,
                 username TEXT NOT NULL,
                 passwordEnc BLOB NOT NULL,
                 userID INTEGER NOT NULL,
                 FOREIGN KEY (userID) REFERENCES users(userID))"""
        with self.connect() as conn:
            conn.execute(sql)
            conn.commit()

    def createUserTable(self):
        sql = """CREATE TABLE IF NOT EXISTS users (  
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    passwordHash BLOB NOT NULL)"""
        with self.connect() as conn:
            conn.execute(sql)
            conn.commit()

    def AddUser(self, username: str, passwordHash: str):
        sql = "INSERT INTO users (username, passwordHash) VALUES (?, ?)"
        try:
            with self.connect() as conn:
                conn.execute(sql,(username, passwordHash))
                conn.commit() 
            return True
        except sqlite3.IntegrityError:
            return False

    def GetPassHash(self, username: str):
        sql = "SELECT passwordHash, userID FROM users WHERE username = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql,(username,))
            row = cursor.fetchone()
            if not row:
                return None
            hashPass = row[0]
            userID = row[1]
            return hashPass, userID
        
    def userExists(self, username: str):
        sql = "SELECT 1 FROM users WHERE username = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql,(username,))
            user = cursor.fetchone()
            return user is not None

    def DropTable (self, tableName): 
        sql = f"DROP TABLE {tableName}"
        with self.connect() as conn:
            conn.execute(sql)
            conn.commit()
        return True

    def createEntrySites(self, site: str, uName: str, passKey, userID: int):
        sql = "INSERT INTO sites  (siteURL, username, passwordEnc, userID) VALUES (?, ?, ?, ?)"
        try:
            with self.connect() as conn:
                conn.execute(sql,(site, uName, passKey, userID))
                conn.commit() 
            return True
        except sqlite3.IntegrityError:
            return False

    def retrieveInfo(self, site: str, userID: int):
        sql = "SELECT username, passwordEnc FROM sites WHERE siteURL = ? AND userID = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql,(site, userID))
            row = cursor.fetchone()
            if row:
                uName, sPass = row
                return uName, sPass
            else:
                return None

    def retrieveInfoFull(self, site: str, userID: int, uname: str):
        sql = "SELECT username, passwordEnc FROM sites WHERE siteURL = ? AND userID = ?  and username = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql,(site, userID, uname))
            row = cursor.fetchone()
            if row:
                uName = row[0]
                return uName
            else:
                return None
    def updatePW(self, password, site: str, uname: str, userID: int):
        sql = "UPDATE sites SET passwordEnc = ? WHERE siteURL = ? AND userID = ? AND username = ?"
        try:
            with self.connect() as conn:
                conn.execute(sql,(password, site, userID, uname))
                conn.commit() 
            return True
        except sqlite3.IntegrityError:
            return False

    def getallSites(self, uID: int):
       sql = "SELECT siteURL AS Website, username AS Username FROM sites WHERE userID = ?"
       headers = ['Website', 'Username']
       rows = []
       with self.connect() as conn:
           for Website, Username in conn.execute(sql, (uID,)):
                rows.append((Website, Username))
       return headers, rows

    def getUser(self, uID: int):
        sql = "SELECT username FROM users WHERE userID = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql,(uID,))
            row = cursor.fetchone()
            if row:
                uName, = row
                return uName
            else:
                return None




