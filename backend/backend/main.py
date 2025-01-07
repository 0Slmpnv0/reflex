from db import DB
from icecream import ic
from db import db

from fastapi import FastAPI
from routers import users, form


app = FastAPI()

app.include_router(users.users)
app.include_router(form.form)


@app.on_event("startup")
def startup():
    db.init()


@app.get("/")
def root():
    return {"root": "root"}
