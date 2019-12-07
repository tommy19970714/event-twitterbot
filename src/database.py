import sqlite3

class Database():
    def __init__(self):
        self.connection = sqlite3.connect("./twitterbot.sqlite")
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS twitter_users")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS twitter_users (id INTEGER PRIMARY KEY AUTOINCREMENT, screen_name VARCHAR(64), flag BOOL)")
    
    def add_user(self, screen_name):
        self.cursor.execute(
            'INSERT OR IGNORE INTO twitter_users (screen_name, flag) VALUES (?, ?)', (screen_name, 0))
        self.connection.commit()
    
    def read_users(self):
        self.cursor.execute('SELECT * FROM twitter_users')
        return self.cursor.fetchall()

    def update_users(self, id, flag):
        self.cursor.execute(
            'UPDATE twitter_users SET flag = ? WHERE id = ?', (flag, id))
        self.connection.commit()


