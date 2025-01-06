from fastapi import APIRouter, Response
from pydantic import BaseModel
import hashlib
import random
from string import ascii_letters
from icecream import ic
from db import db


def gen_salt():
    letters = list(ascii_letters)
    salt = ""
    for _ in range(10):
        salt += random.choice(letters)
    return salt


class User(BaseModel):
    login: str
    username: str
    password: str
    field_settings: dict | None = None


users = APIRouter(prefix="/users")


@users.post("/add_user")
def new_user(user: User, response: Response):
    global db
    salt = gen_salt()
    str_to_hash = user.password + salt

    password = hashlib.sha256(str_to_hash.encode(encoding="UTF-8")).hexdigest()
    status, result = db.add_user(
        user.username, user.login, password, salt, user.field_settings
    )
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
