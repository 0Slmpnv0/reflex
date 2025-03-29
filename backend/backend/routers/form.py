from fastapi import APIRouter, Cookie
from db import db
from icecream import ic
from typing import Annotated, Optional, Literal
from security import validate_cookie
from pydantic import BaseModel, Field
from config import invalid_cookie_message


class Display(BaseModel):
    is_display_field: bool
    is_positive: Optional[bool] = None  # experimental. Won't be used yet


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
    display: Optional[Display] = Field(
        default=False,
        title="Will this field be displayed on the calendar page?"
    )


form = APIRouter(prefix="/form")


@form.post("/update_form_settings")
def update_form(
    user_id, 
    new_settings: list[FieldSettings], 
    auth_cookie: Annotated[str, Cookie()]
    ):
    status, res = validate_cookie(user_id, auth_cookie)
    if not res:
        return {"status": 403, "message": invalid_cookie_message}
    if status == 200 and res:
        new_settings_json = '['
        for field in new_settings:
            new_settings_json += field.model_dump_json() + ","
        new_settings_json = new_settings_json[:-1] + "]"
        status, msg = db.update_field_settings(user_id, new_settings_json)
        return {"status": status, "message": msg}
    else:
        return {"status": status, "message": res}


@form.get("/get_form")
def get_form_settings(
    user_id, 
    auth_cookie: Annotated[str, Cookie()]
    ):
    status, res = validate_cookie(user_id, auth_cookie)
    if not res:
        return {"status": 403, "message": invalid_cookie_message}
    if status == 200 and res:
        status, res = db.get_field_settings(user_id)
    return {"status": status, "form": res}
