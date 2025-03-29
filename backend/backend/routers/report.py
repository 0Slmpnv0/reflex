from fastapi.routing import APIRouter
from fastapi import Cookie
from db import db
from pydantic import BaseModel
from security import validate_cookie
from datetime import date
from typing import Annotated
from icecream import ic
from config import invalid_cookie_message

class Metric(BaseModel):
    name: str
    value: str | int | bool


report = APIRouter(prefix='/report')

@report.post('/push_report')
def add_rep(
    user_id, 
    auth_cookie: Annotated[str, Cookie()], 
    report: list[Metric],
    rep_date: date
    ):
    status, res = validate_cookie(user_id, auth_cookie)
    if status == 200: 
        if res:
            try:
                report_json = '['
                for metric in report:
                    report_json += metric.model_dump_json() + ','
                report_json = report_json[:-1] + ']'
                status, res = db.add_report(user_id, report_json, rep_date)
                if status == 200:
                    return {"status": 200, "message": res}
                else:
                    return {"status": status, "message": res}
            except Exception as e:
                ic(e)
                return {"status": 500, "message": str(e)}
        else:
            return {"status": 403, "message": invalid_cookie_message}
    else: 
        return {"status": status, "message": res}

@report.get('/get_report')
def get_rep(
    user_id,
    auth_cookie: Annotated[str, Cookie()],
    date: date
):
    status, res = validate_cookie(user_id, auth_cookie)
    if status == 200:
        if res:
            status, res = db.get_report(user_id, str(date))
            if status == 200:
                return {'status': 200, "report": res}
        else:
            return {"status": 403, "message": invalid_cookie_message }
    return {"status": status, "message": res}
