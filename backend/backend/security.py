from string import ascii_letters
import secrets
import random
from icecream import ic
from redis_db import redis
import hashlib
from db import db
from redis_db import redis


def validate_cookie(user_id, cookie_to_check):
    try:
        real_auth_cookie = redis.get(f"{user_id}_session_key").decode()
        if real_auth_cookie == cookie_to_check:
            return 200, True
        else:
            return 200, False
    except Exception as e:
        return 500, str(e)


def add_cookie(user_id) -> str:
    session_token = secrets.token_hex(16)
    try:
        redis.set(f"{user_id}_session_key", session_token, ex=20 * 86400)
        return 200, session_token
    except Exception as e:
        ic(e)
        return 500, str(e)


def gen_salt():
    letters = list(ascii_letters)
    salt = ""
    for _ in range(10):
        salt += random.choice(letters)
    return salt


def hash_a_password(password):
    salt = gen_salt()
    str_to_hash = password + salt
    return hashlib.sha256(str_to_hash.encode(encoding="UTF-8")).hexdigest(), salt


def compare_passwords(login, password_to_check):
    status, res = db.get_password_data(login)
    if status != 200:
        return {"status": status, "msg": res[0]}
    actual_password_hash, salt = res
    return (
        hashlib.sha256((password_to_check + salt).encode(encoding="UTF-8")).hexdigest()
        == actual_password_hash
    )
