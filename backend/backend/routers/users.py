from fastapi import APIRouter, Response
from pydantic import BaseModel, Field
import hashlib
import random
from string import ascii_letters
from icecream import ic
from db import db
from typing import Optional, Dict
from redis_db import redis
import secrets
from fastapi.responses import JSONResponse


def gen_salt():
    letters = list(ascii_letters)
    salt = ""
    for _ in range(10):
        salt += random.choice(letters)
    return salt


class FieldSettings(BaseModel):
    name: str
    type: str
    options: Optional[list[str]]
    display: Dict[str, bool]


class User(BaseModel):
    login: str
    username: str
    password: str


users = APIRouter(prefix="/users")


@users.post("/add_user")
def new_user(user: User, response: Response):
    global db
    salt = gen_salt()
    str_to_hash = user.password + salt

    password = hashlib.sha256(str_to_hash.encode(encoding="UTF-8")).hexdigest()
    status, result = db.add_user(user.username, user.login, password, salt)
    return {"status": status, "result": result}


@users.get("/")
def debug_func_delete_later(user_id: str):
    status, res = db.get_user(user_id)
    user_data = (
        {
            "id": res[0],
            "login": res[1],
            "username": res[2],
            "field_settings": res[3],
        }
        if status == 200
        else res
    )
    return {"status": status, "response": user_data}


@users.get("/validate_login")
def validate_login(login):
    ic(login)
    status, result = db.check_login(login)
    if status == 500:
        return {status: 500}
    return {"status": status, "availiable": not result}


@users.post("/password_login")
def auth_a_user(login, password):
    status, salt = db.get_salt(login)
    if status == 500:
        return {"status": 500}
    password += salt
    password = hashlib.sha256(password.encode("UTF-8")).hexdigest()
    status, result = db.check_password(login, password)
    if status == 500:
        return {"status": 500}

    resp = JSONResponse({"status": status, "result": result})
    status, ret = db.get_user_id(login)
    if status != 200:
        return 500, ret
    user_id = ret
    if not redis.exists(f"{user_id}_session_key"):
        session_token = secrets.token_hex(16)
        ic("session", session_token)
        resp.set_cookie(key=f"{user_id}_session_key", value=session_token)
        ic("still ok")
        try:
            redis.set(f"{user_id}_session_key", session_token, ex=20 * 86400)
        except Exception as e:
            ic(e)

    return resp
