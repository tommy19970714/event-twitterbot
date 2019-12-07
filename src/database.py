import sqlite3


class Database():
    def __init__(self, filepath='./twitterbot.sqlite', tablename='twitter_users'):
        self.filepath = filepath
        self.tablename = tablename

        self.connection = sqlite3.connect(self.filepath)
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS {}".format(self.tablename))
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                screen_name VARCHAR(64), 
                flag BOOL)""".format(self.tablename))

    def add_user(self, screen_name):
        """
        >>> db = Database(tablename='test_twitter_users')
        >>> db.add_user('test_user1')
        >>> db.count_users()
        [(1,)]
        """
        self.cursor.execute(
            'INSERT OR IGNORE INTO {} (screen_name, flag) VALUES (?, ?)'.format(self.tablename), (screen_name, 0))
        self.connection.commit()

    def read_users(self):
        self.cursor.execute('SELECT * FROM {}'.format(self.tablename))
        return self.cursor.fetchall()

    def count_users(self):
        self.cursor.execute('SELECT count(*) FROM {}'.format(self.tablename))
        return self.cursor.fetchall()

    def update_users(self, id, flag):
        self.cursor.execute(
            'UPDATE {} SET flag = ? WHERE id = ?'.format(self.tablename), (flag, id))
        self.connection.commit()


if __name__ == '__main__':
    import doctest
    doctest.testmod()