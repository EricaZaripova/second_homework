import math
import sqlite3
import time


class FlaskDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        """Returns all menu items from mainmenu table."""
        query = "SELECT * from mainmenu"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"Unexpected exception {e}")
        return []

    def add_user(self, email, password):
        created_at = math.floor(time.time())
        try:
            self.__cur.execute(
                "INSERT INTO users VALUES (NULL, ?, ?, ?)",
                (email, password, created_at)
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def get_users(self):
        try:
            self.__cur.execute(
                "SELECT * FROM users"
            )
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Exception in getting posts list: {e}")
        return []

    def get_password_hash(self, email):
        try:
            self.__cur.execute(
                f"SELECT * FROM users WHERE email = '{email}'"
            )
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Exception in getting password by email {email}: {e}")
        return False
