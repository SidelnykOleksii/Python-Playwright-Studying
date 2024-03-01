import sqlite3


class DataBase:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)

    def check_user_exist(self, username: str, email: str):
        c = self.connection.cursor()
        c.execute('SELECT EXISTS(SELECT id FROM auth_user WHERE username=? AND email=?)', (username, email))
        return c.fetchone()

    def delete_user(self, username: str):
        c = self.connection.cursor()
        c.execute('DELETE FROM auth_user WHERE username=?', (username,))
        self.connection.commit()

    def close(self):
        self.connection.close()
