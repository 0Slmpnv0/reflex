from fastapi import APIRouter
from db import db
from icecream import ic


form = APIRouter(prefix="/form")


@form.get("/get_form")
def get_form_settings(user_id):
    status, res = db.get_field_settings(user_id)
    return {"status": status, "result": res}
