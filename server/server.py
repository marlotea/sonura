from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os
import sqlalchemy

# our modules
from routes.routes import check_version
from db.dbConnect import Session_Local, engine, create_tables
from spotify.utils import *

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


# this shit will be migrated to a routes folder later on, just here for testing and easy access
@app.get("/test")
def get_spotify_data():
    id, secret = get_client()
    return {"client_id": id, "client_secret": secret}


@app.get("/spotify-token")
def get_spotify_token():
    token = get_token()
    return {"token": token}


@app.get("spotify-auth")
def get_spotify_auth():
    token = get_token()
    auth_token = get_auth_header(token)
    return {"auth_token": auth_token}


@app.get("/artist")
def search_artist(artist_name: Artist):
    token = get_token()
    try:
        name = serach_for_artist(token, artist_name)
        return {"res": name}
    except Exception as e:
        return {"Error": e}


@app.get("/artist-id")
def get_id_artist(artist_name: Artist):
    token = get_token()
    id = get_artist_id(token, artist_name)
    return {"id": id}


@app.get("/artist-top-tracks")
def get_top_tracks(artist_name: Artist):
    token = get_token()
    id = get_artist_id(token, artist_name)
    top_tracks = get_songs_by_artist(token, id)
    return {"result": top_tracks}


@app.get("/db")
async def check_db():
    info = await check_version()
    return info


@app.get("/playlists")
async def get_playlists():
    res = await get_user_playlist()
    return {"playlists": res}
