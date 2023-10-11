# import gspread
# from config import JSON_KEY, SHEET_KEY
#
# gc = gspread.service_account(filename=JSON_KEY)
# sh = gc.open_by_key(key=SHEET_KEY)
# worksheet = sh.get_worksheet(0)

import sqlite3
from jsonwriter import *


class Database:

    def __init__(self):
        self.db = sqlite3.connect(database='database.sqlite')
        self.c = self.db.cursor()


    def create_table(self, table):
        try:
            self.c.execute(f'''CREATE TABLE {table} (
        clicks integer,
        clicks_day integer,
        clicks_week integer,
        clicks_month integer,
        day integer,
        active_users integer,
        banned_users integer
)''')
            self.db.commit()

        except Exception as e:
            print('[!] Database error:', e)


    def add_value(self, table, values):
        try:
            self.c.execute(f"INSERT INTO {table} VALUES ({values})")
            self.db.commit()
            print(f'[*] Added value to the "{table}": {values}')
        except Exception as e:
            print('[!] Database error:', e)


    def select_value(self, table, keys, where=''):
        try:
            if where == '':
                self.c.execute(f"SELECT {keys} FROM {table}")
                show = self.c.fetchall()
                return show
            else:
                self.c.execute(f"SELECT {keys} FROM {table} WHERE {where}")
                show = self.c.fetchall()
                return show
        except Exception as e:
            print('[!] Database error:', e)


    def delete_value(self, table, where='---'):
        try:
            self.c.execute(f"DELETE FROM {table} WHERE {where}")
            self.db.commit()
            print(f'[*] Deleted "{where}" from "{table}"')
        except Exception as e:
            print('[!] Database error:', e)


    def update_value(self, table, key, where='---'):
        try:
            self.c.execute(f"UPDATE {table} SET {key} WHERE {where}")
            self.db.commit()
            print(f'[*] Updated "{where}" from "{table}": {key}')
        except Exception as e:
            print('[!] Database error:', e)

    def drop_table(self, table):
        try:
            self.c.execute(f'DROP TABLE {table}')
            self.db.commit()
            print(f'[*] Dropped "{table}"')
        except Exception as e:
            print('[!] Database error:', e)

    def close_db(self):
        self.db.close()


if __name__ == '__main__':
    database = Database()
    # database.drop_table(table='stats')
    # database.add_value(table='stats', values="0, 0, 0, 0, 0, 0, 0")
    # database.create_table(table='stats')
    # a = database.select_value(table='users', keys='rowid, *', where="user_id = 972383332")
    # print(a)
    # database.update_value(table='stats', key='clicks = clicks + 1', where='rowid = 1')

    # level = database.select_value(table='users', keys='*', where=f'')
    # print(level)

    print(len(database.select_value(table='users', keys='*', where='')))

    # database.update_value(table='users', key="'1' = ''", where="user_id = 972383332")
    # a = database.select_value(table='users', keys='rowid, *')
    # print(a)
    # database.select_value(table='users', keys='rowid, *', where="")
    # database.delete_value(table='users', where='rowid = 1')
    # a = database.select_value(table='users', keys='rowid, *')
    # print(a)