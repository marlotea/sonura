from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os

from routes import check_version

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Success"}

@app.get("/db")
async def check_db():
    check_version()
    return {"message" : "success"}