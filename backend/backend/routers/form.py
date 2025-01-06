from fastapi import APIRouter
from db import db
from icecream import ic
import hashlib


form = APIRouter(prefix="/form")


@form.get("/validate_login")
def validate_login(login):
    ic(login)
    status, result = db.check_login(login)
    if status == 500:
        return {status: 500}
    return {"status": status, "availiable": not result}


@form.post("/check_password")
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
