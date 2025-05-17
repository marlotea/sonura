from typing import Union, Annotated
from fastapi import FastAPI, Header, Request, Response
import requests as req
import os
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

# our modules
from routes.routes import check_version
from db.dbConnect import Session_Local, engine, create_tables
from spotify.utils import *
from routes.spotify_routes import router as spotify_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY_MEOW"), 
    max_age=3600 * 24 * 7, # 1 week
    same_site="lax",
    https_only=not os.getenv("ENVIRONMENT") == "dev"
)

app.include_router(spotify_router, prefix="/spotify")

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

@app.get("/db")
async def check_db():
    info = await check_version()
    return info

@app.get("/get_recs")
def get_rec():
    return {
        "message" : "success"
    }
