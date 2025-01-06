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

    def add_user(self, username, login, cached_password, salt, field_settings=None):
        try:
            fields = field_settings if bool(field_settings) else None
            ic(type(field_settings))
            ic(type(fields))
            ic(cached_password)
            ic(login)
            self.cursor.execute(
                """INSERT INTO users (username, login, cached_password, salt, field_settings) 
                VALUES (%s, %s, %s, %s, %s)""",
                (username, login, cached_password, salt, fields),
            )
        except Exception as e:
            ic(str(e))
            self.connection.rollback()
            return 500, str(e)

        self.connection.commit()

        return 200, "succeeded!"

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

    def get_salt(self, login):

        try:
            self.cursor.execute("""SELECT salt FROM users WHERE login = %s""", (login,))
            return 200, self.cursor.fetchone()[0]
        except Error as e:
            self.connection.rollback()
            print(e)
            return 500, ""

    def check_password(self, login, cached_password):
        try:
            query = """
                SELECT 1 
                FROM users 
                WHERE login = %s AND cached_password = %s
            """
            ic(login, cached_password)
            self.cursor.execute(query, (login, cached_password))

            result = self.cursor.fetchone()
            ic(str(result))
            return 200, str(result) == "(1,)"

        except Exception as e:
            self.connection.rollback()
            ic(e)
            return 500, False


db = DB(PG_CONNECT_DATA)
