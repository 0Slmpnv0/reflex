from fastapi import APIRouter, Response, Path
from pydantic import BaseModel
from security import hash_a_password, add_cookie, compare_passwords
from icecream import ic
from db import db
from typing import Union
from config import cookie_expiration


class User(BaseModel):
    login: str
    username: str
    password: str


users = APIRouter(prefix="/users")


@users.post("/add_user")
def new_user(user: User, response: Response):
    password, salt = hash_a_password(user.password)
    status, result = db.add_user(user.username, user.login, password, salt)
    return {"status": status, "result": result}


@users.get("/")
def get_user_data(user_id: str):  # dev func. Not for the prod!
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
def auth_a_user(
    login, 
    password, 
    remember_me: Union[bool, str]
    ):

    if not compare_passwords(login, password):
        return {"status": 403, "msg": "Forbidden! Wrong password"}
    content = {"status": 200, "message": "Authorised!"}
    if remember_me == 'true':
        response = Response()
        status, res = db.get_user_id(login)
        if status != 200:
            return {"status": status, "messge": res}
        user_id = res
        status, resp = add_cookie(user_id)
        if status != 200:
            return {"status":status, "message": resp}
        response.set_cookie(
            key="auth_cookie",
            value=resp, 
            max_age=cookie_expiration, 
            samesite="strict", 
            httponly=True
        )
        response.content = content
        return response
    return content
