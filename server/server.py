from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os
import sqlalchemy

# our modules
from routes.routes import check_version
from db.dbConnect import Session_Local, engine, create_tables
from spotify_endpoints.spotify_endpoints import get_client, get_token

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        with engine.connect() as connection:
            print("Connected to db")
            create_tables()
    except Exception as e:
        print(f"Failed to connect to db. Error: {e}")

@app.on_event("shutdown")
def shutdown():
    print("Shutting down db")

@app.get("/")
async def root():
    return {"message": "Success"}

@app.get("/test")
def get_spotify_data():
    id, secret = get_client()
    return {
        "client_id" : id,
        "client_secret" : secret
    }

@app.get("/spotify-token")
def get_spotify_token():
    token = get_token()
    return {"token" : token}


@app.get("/db")
async def check_db():
    info = await check_version()
    return info
