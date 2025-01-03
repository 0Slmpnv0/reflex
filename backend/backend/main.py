from db import DB
from icecream import ic
import hashlib
import random
from string import ascii_letters

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from dotenv import get_key
from config import PG_CONNECT_DATA


class User(BaseModel):
    login: str
    username: str
    password: str
    field_settings: dict | None = None


class NewReportModel(BaseModel):
    user_id: int
    report: dict


def gen_salt():
    letters = list(ascii_letters)
    salt = ""
    for _ in range(10):
        salt += random.choice(letters)
    return salt


db = DB(PG_CONNECT_DATA)
app = FastAPI()


@app.on_event("startup")
def startup():
    db.init()


@app.post("/add_user")
def new_user(user: User, response: Response):
    salt = gen_salt()
    str_to_hash = user.password + salt
    ic(salt, user.password)

    password = hashlib.sha256(str_to_hash.encode(encoding="UTF-8")).hexdigest()
    ic(password)
    status, result = db.add_user(
        user.username, user.login, password, salt, user.field_settings
    )
    return {"status": status, "result": result}


@app.post("/add_report")
def new_report(new_report: NewReportModel):
    status = db.add_report(new_report.user_id, new_report.report)
    return {"status": status}


@app.get("/users")
def debug_func_delete_later(user_id: str):
    status, data = db.get_user(user_id)
    return {"status": status, "user_data": data}


@app.get("/form/validate_login")
def validate_login(login):
    ic(login)
    status, result = db.check_login(login)
    if status == 500:
        return {status: 500}
    return {"status": status, "valid": result}


@app.post("/form/check_password")
def check_password(login, password):
    status, salt = db.get_salt(login)
    if status == 500:
        return {"status": 500}
    password += salt
    password = hashlib.sha256(password.encode("UTF-8")).hexdigest()
    status, result = db.check_password(login, password)
    if status == 500:
        return {"status": 500}
    return {"status": status, "result": result}
