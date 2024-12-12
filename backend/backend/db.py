from config import PG_CONNECT_DATA
from psycopg import connect


class DB:
    def __init__(self, conn_data):
        self.connection = connect(conn_data)
        self.cursor = self.connection.cursor()

    def init(self):
        try:
            self.cursor.execute(
                """--sql
            CREATE TABLE IF NOT EXISTS users (
                user_id integer GENERATED ALWAYS AS IDENTITY (START WITH 100000) PRIMARY KEY,
                username char(15),
                login char(15) UNIQUE,
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
        try:
            self.cursor.execute(
                """--sql
                SELECT user_id, username, login, field_settings FROM users WHERE user_id = %s;
            """,
                (uid,),
            )
            ret = self.cursor.fetchone()

        except Exception as e:
            print(e)
            return 500

        self.connection.commit()
        return 200, ret

    def add_user(self, username, login, cached_password, salt, field_settings=None):
        try:
            if field_settings:
                self.cursor.execute(
                    """INSERT INTO users (username, login, cached_password, salt, field_settings) VALUES (%s, %s, %s, %s, %s)""",
                    (username, login, password, field_settings),
                )
            else:
                self.cursor.execute(
                    """INSERT INTO users (username, login, cached_password, salt) VALUES (%s, %s, %s, %s)""",
                    (username, login, cached_password, salt),
                )
        except Exception as e:
            print(e)
            return 500

        self.connection.commit()

        return 200

    def add_report(self, user_id, report):
        try:
            self.cursor.execute(
                """INSERT INTO reps (user_id, report) VALUES (%s, %s)""",
                (user_id, report),
            )
        except Exception as e:
            print(e)
            return 500
        self.connection.commit()

        return 200
