from config import PG_CONNECT_DATA
from psycopg import connect
from icecream import ic
import atexit


class DB:
    def __init__(self, conn_data):
        self.connection = connect(conn_data)
        self.cursor = self.connection.cursor()
        atexit.register(self.connection.commit)
        atexit.register(self.connection.close)

    def init(self):
        try:
            self.cursor.execute(
                """--sql
            CREATE TABLE IF NOT EXISTS users (
                user_id integer GENERATED ALWAYS AS IDENTITY (START WITH 100000) PRIMARY KEY,
                username VARCHAR(15),
                login VARCHAR(15) UNIQUE,
                cached_password char(64),
                salt char(10),
                field_settings json
            );
            """
            )
            self.cursor.execute(
                """--sql
                CREATE TABLE IF NOT EXISTS reps (
                user_id integer PRIMARY KEY,
                report json
            );
            """
            )

            self.connection.commit()
            return 200

        except Exception as e:
            print(e)
            return 500

    # users related querys

    def get_user(self, uid):
        ic("getting a user...")
        try:
            self.cursor.execute(
                """--sql
                SELECT user_id, login, username, field_settings FROM users WHERE user_id = %s;
            """,
                (uid,),
            )
            ret = self.cursor.fetchone()

        except Exception as e:
            self.connection.rollback()
            print(e)
            return 500, str(e)

        if not ret:
            return 404, "probably user does not exsist"
        self.connection.commit()
        return 200, ret

    def add_user(self, username, login, cached_password, salt):
        try:
            self.cursor.execute(
                """INSERT INTO users (username, login, cached_password, salt) 
                VALUES (%s, %s, %s, %s)""",
                (username, login, cached_password, salt),
            )
        except Exception as e:
            ic(e)
            self.connection.rollback()
            return 500, str(e)

        self.connection.commit()

        return 200, "succeeded!"

    def check_login(self, login):
        try:
            self.cursor.execute(
                """SELECT 1 
            FROM users 
            WHERE login = %s""",
                (login,),
            )
            return 200, str(self.cursor.fetchone()) == "(1,)"
        except Error as e:
            self.connection.rollback()
            print(e)
            return 500, ""

    def get_password_data(self, login):

        try:
            self.cursor.execute(
                """SELECT cached_password, salt FROM users WHERE login = %s""", (login,)
            )
            res = self.cursor.fetchone()
            return 200, (res[0], res[1])

        except Exception as e:
            self.connection.rollback()
            ic(e)
            return 500, (str(e), "")

    def get_user_id(self, login):
        try:
            self.cursor.execute(
                """--sql 
                SELECT user_id 
                FROM users 
                WHERE login = %s""",
                (login,),
            )
            ret = self.cursor.fetchone()
            if not ret:
                return 404, "Probably no such user"
            return 200, ret[0]
        except Exception as e:
            ic(e)
            return 500, str(e)

    # form related querys


    def update_field_settings(self, user_id, new_settings):
        try:
            self.cursor.execute(
                """--sql
            UPDATE users
            SET field_settings = %s
            WHERE user_id = %s;
             """,
                (new_settings, user_id),
            )

            return 200, "succeeded!"
        except Exception as e:
            self.connection.rollback()
            ic(e)
            return 500, str(e)


    def get_field_settings(self, user_id):
        try:
            self.cursor.execute(
                """SELECT field_settings FROM users WHERE user_id = %s""", (user_id,)
            )
            return 200, self.cursor.fetchone()
        except Exception as e:
            ic(e)
            return 500, str(e)

    def add_report(self, user_id, report):
        try:
            self.cursor.execute(
                """INSERT INTO reps (user_id, report) 
                VALUES (%s, %s)""",
                (user_id, report),
            )
        except Exception as e:
            self.connection.rollback()
            print(e)
            return 500
        self.connection.commit()

        return 200


db = DB(PG_CONNECT_DATA)
