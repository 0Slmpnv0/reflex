from dotenv import get_key

PG_CONNECT_DATA = f"host='pg' dbname='test' user='{get_key('.env', 'PG_USER')}' password='{get_key('.env', 'PG_PASSWORD')}' port='5432'"
