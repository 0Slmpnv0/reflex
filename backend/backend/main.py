from db import DB

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
    field_settings: dict | None


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


@app.get("/")
def root():
    return {"example": "api"}


@app.post("/add_user")
def new_user(user: User, response: Response):
    salt = gen_salt()
    str_to_hash = user.password + salt

    password = hashlib.sha256(str_to_hash.encode(encoding="UTF-8")).hexdigest()
    status = db.add_user(user.username, user.login, password, salt, user.field_settings)
    return {"status": status}


@app.post("/add_report")
def new_report(new_report: NewReportModel):
    status = db.add_report(new_report.user_id, new_report.report)
    return {"status": status}


@app.get("/users")
def get_user(user_id: str):
    return db.get_user(user_id)
