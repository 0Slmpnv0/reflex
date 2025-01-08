from dotenv import get_key

PG_CONNECT_DATA = f"host='pg' dbname='test' user='{get_key('.env', 'POSTGRES_USER')}' password='{get_key('.env', 'POSTGRES_PASSWORD')}' port='5432'"
REDIS_CONNECT_DATA = {
    "host": "redis",
    "port": 6379,
    "db": 0,
    "username": get_key(".env", "REDIS_USER"),
    "password": get_key(".env", "REDIS_PASSWORD"),
}
