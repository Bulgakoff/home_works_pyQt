import sqlite3
import time
from dataclasses import dataclass

from icecream import ic

connection = None
class ClientStorage:
    drop_ulp = 'DROP TABLE IF EXISTS user_login_password'
    create_ulp = """
                            create table if not exists user_login_password (
                                id  INTEGER primary key,
                                user_login TEXT NOT NULL,
                                user_password TEXT NOT NULL
                            );
                """
    drop_cli_history = 'DROP TABLE IF EXISTS cli_history'
    create_cli_history = """
                            create table if not exists cli_history (
                                id  INTEGER primary key,
                                connect_time time NOT NULL,
                                address TEXT NOT NULL,
                                user_id INTEGER  NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES user_login_password(id)
                            );
                """

    insert_col_ulp = """insert into user_login_password (user_login, user_password)
        VALUES (?, ?)"""

    insert_col_cli_history = """insert into cli_history (connect_time, address, user_id)
        VALUES (?, ?, ?)"""
    def get_conn(self):
        global connection
        if connection is None:
            connection = sqlite3.connect("anketa.db")
            connection.row_factory = sqlite3.Row
        return connection

    def create_ClientInfo_or_ClientStorage(self, force: bool = False):
        conn = self.get_conn()
        c = conn.cursor()
        if force:
            c.execute(self.drop_ulp)
            c.execute(self.drop_cli_history)
        else:
            c.execute(self.create_ulp)
            c.execute(self.create_cli_history)
            # сохрнить изменения
            conn.commit()

    def add_login_info(self, user_login: str, user_password: str):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(self.insert_col_ulp, (user_login, user_password))
        c.execute("SELECT * FROM user_login_password")
        for row in c:
            for value in row:
                ic(value)
        print()
        conn.commit()

    def add_cli_history(self, connect_time: time, address: str, user_id: int):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(self.insert_col_cli_history, (connect_time, address, user_id))
        c.execute("SELECT * FROM cli_history")
        for row in c:
            for value in row:
                ic(value)
        print()
        conn.commit()


if __name__ == '__main__':
    spam = ClientStorage()
    spam.create_ClientInfo_or_ClientStorage()
    spam.add_login_info(user_login='ppp', user_password='888')
    spam.add_cli_history(connect_time=time.ctime(), address='198.208.50.444', user_id=100)


