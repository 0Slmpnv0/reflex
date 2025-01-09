from fastapi import APIRouter, Cookie
from db import db
from icecream import ic
from typing import Annotated, Optional, Literal
from security import validate_cookie
from pydantic import BaseModel, Field


class Display(BaseModel):
    is_display_field: bool
    is_positive: Optional[bool]  # experimental. Won't be used yet


class FieldSettings(BaseModel):
    name: str
    type: Literal["tag", "number", "checkbox", "percent", "unselected"]
    options: Optional[list[str]] = Field(
        default=None,
        title="Possible tags",
        description="Only required if the type of a field is 'tag'. Represents the possible options, that were already used",
    )
    is_required: Optional[bool] = Field(
        default=False,
        title="Is the field required to be filled?",
        description="Experimental field. Not required yet",
    )  # experimental too
    display: Optional[Display]


form = APIRouter(prefix="/form")


@form.post("/update_form_settings")
def update_form(
    user_id, new_settings: FieldSettings, auth_cookie: Annotated[str, Cookie()]
):
    status, res = validate_cookie(user_id, auth_cookie)
    if not res:
        return {"status": 403, msg: "Forbidden! Cookies do not match"}
    if status == 200 and res:
        status, msg = db.update_field_settings(user_id, new_settings.model_dump_json())
        return {"status": status, "msg": msg}


@form.get("/get_form")
def get_form_settings(user_id, auth_cookie: Annotated[str, Cookie()]):
    status, res = validate_cookie(user_id, auth_cookie)
    if not res:
        return {"status": 403, "msg": "Forbidden! Cookies do not match"}
    if status == 200 and res:
        status, res = db.get_field_settings(user_id)
    return {"status": status, "res": res}
