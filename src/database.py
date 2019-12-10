import sqlite3


class Database():
    def __init__(self, filepath='./twitterbot.sqlite', tablename='twitter_users', drop_anyway=False):
        self.filepath = filepath
        self.tablename = tablename

        self.connection = sqlite3.connect(self.filepath)
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        if drop_anyway:
            self.cursor.execute("DROP TABLE IF EXISTS {}".format(self.tablename))
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                screen_name VARCHAR(64) UNIQUE, 
                friends INTEGER,
                followers INTEGER,
                followed BOOL,
                followed_at TEXT,
                unfollowed BOOL,
                unfollowed_at TEXT,
                update_at TEXT)""".format(self.tablename))

    def add_user(self, screen_name, friends, followers, followed, followed_at, unfollowed, unfollowed_at, update_at):
        """
        >>> db = Database(tablename='test_twitter_users', drop_anyway=True)
        >>> db.add_user('test_user1', 0, 0, False,'', False, '', '')
        >>> db.count_users()
        [(1,)]
        """
        self.cursor.execute(
            """INSERT OR IGNORE INTO {} 
            (screen_name, friends, followers, followed, followed_at, unfollowed, unfollowed_at, update_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""".format(self.tablename), 
            (screen_name, friends, followers, followed, followed_at, unfollowed, unfollowed_at, update_at))
        self.connection.commit()

    def read_users(self, count=10):
        """
        >>> db = Database(tablename='test_twitter_users', drop_anyway=True)
        >>> db.add_user('u1', 0, 0, False, '', False, '', '')
        >>> db.add_user('u2', 9, 1, False, '', False, '', '')
        >>> db.add_user('u3', 3, 1, False, '', False, '', '')
        >>> db.read_users()
        [(2, u'u2', 9, 1), (3, u'u3', 3, 1), (1, u'u1', 0, 0)]
        """
        self.cursor.execute(
            """SELECT id, screen_name, friends, followers FROM {}
            WHERE followed!=1 OR followed IS NULL ORDER BY friends / (followers + 1) DESC LIMIT {}""".format(self.tablename, count))
        return self.cursor.fetchall()

    def read_unfollow_users(self, count=10):
        """
        >>> db = Database(tablename='test_twitter_users', drop_anyway=True)
        >>> db.add_user('u1', 0, 0, True, '2019-12-07 09:23:13', False, '', None)
        >>> db.add_user('u2', 9, 1, True, '2019-12-08 09:23:13', False, '', None)
        >>> db.add_user('u3', 3, 1, True, '2019-12-09 09:23:13', False, '', None)
        >>> db.read_unfollow_users()
        [(1, u'u1', 0, 0), (2, u'u2', 9, 1), (3, u'u3', 3, 1)]
        """
        self.cursor.execute(
            """SELECT id, screen_name, friends, followers FROM {}
            WHERE followed=1 AND unfollowed=0 ORDER BY followed_at LIMIT {}""".format(self.tablename, count))
        return self.cursor.fetchall()

    def follow_count_today(self):
        """
        >>> db = Database(tablename='test_twitter_users', drop_anyway=True)
        >>> db.add_user('u1', 0, 0, False, '2019-12-07 09:23:13', False, '', '')
        >>> db.add_user('u2', 9, 1, False, '2019-12-08 09:23:13', False, '', '')
        >>> db.add_user('u3', 3, 1, False, '2019-12-09 09:23:13', False, '', '')
        >>> db.follow_count_today()
        [(0,)]
        """
        self.cursor.execute(
            """
            SELECT count(followed_at)
            FROM {} 
            WHERE DATE(followed_at) = DATE('now')
            """.format(self.tablename))
        return self.cursor.fetchall()

    def unfollow_count_today(self):
        """
        >>> db = Database(tablename='test_twitter_users', drop_anyway=True)
        >>> db.add_user('u1', 0, 0, False, '', False, '2019-12-07 09:23:13', '')
        >>> db.add_user('u2', 9, 1, False, '', False, '2019-12-08 09:23:13', '')
        >>> db.add_user('u3', 3, 1, False, '', False, '2019-12-09 09:23:13', '')
        >>> db.unfollow_count_today()
        [(0,)]
        """
        self.cursor.execute(
            """
            SELECT count(unfollowed_at)
            FROM {} 
            WHERE DATE(unfollowed_at) = DATE('now')
            """.format(self.tablename))
        return self.cursor.fetchall()


    def count_users(self):
        self.cursor.execute('SELECT COUNT(*) FROM {}'.format(self.tablename))
        return self.cursor.fetchall()

    def update_users(self, id, flag):
        self.cursor.execute(
            'UPDATE {} SET flag = ? WHERE id = ?'.format(self.tablename), (flag, id))
        self.connection.commit()

    def update_user(self, screen_name, key, value):
        self.cursor.execute(
            """UPDATE {} SET {} = ? WHERE screen_name = ?""".format(self.tablename, key), 
            (value, screen_name))
        self.connection.commit()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
