from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os
import sqlalchemy

from routes.routes import check_version
from db.dbConnect import Session_Local, engine

app = FastAPI()

@app.on_event("startup")
def startup():
    try:
        with engine.connect() as connection:
            print("Connected to db")
    except Exception as e:
        print(f"Failed to connect to db. Error: {e}")

@app.on_event("shutdown")
def shutdown():
    print("Shutting down db")

@app.get("/")
async def root():
    return {"message": "Success"}


@app.get("/db")
async def check_db():
    info = await check_version()
    return info
