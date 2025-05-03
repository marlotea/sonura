from typing import Union, Annotated
from fastapi import FastAPI, Header, Request, Response
import requests as req
import os
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware

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


# this shit will be migrated to a routes folder later on, just here for testing and easy access
@app.get("/test")
def get_spotify_data():
    id, secret = get_client()
    return {"client_id": id, "client_secret": secret}


@app.get("/spotify-token")
def get_spotify_token():
    token = get_token()
    return {"token": token}


@app.get("/spotify-auth")
def get_spotify_auth():
    token = get_token()
    auth_token = get_auth_header(token)
    return {"auth_token": auth_token}


@app.get("/artist")
def search_artist(artist_name: Artist):
    token = get_token()
    try:
        name = search_for_artist(token, artist_name)
        return {"res": name}
    except Exception as e:
        return {"Error": e}


@app.get("/artist-id")
def get_id_artist(artist_name: Artist):
    token = get_token()
    id = get_artist_id(token, artist_name)
    return {"id": id}


@app.get("/artist-top-tracks")
def get_artists_top_tracks(artist_name: Artist):
    token = get_token()
    id = get_artist_id(token, artist_name)
    top_tracks = get_songs_by_artist(token, id)
    return {"result": top_tracks}


@app.get("/db")
async def check_db():
    info = await check_version()
    return info


# @app.get("/login")
# def log_in():
#     return login()


# @app.get("/callback")
# async def callback(request: Request, response: Response):
#     return await callback_func(request, response)


# @app.get("/playlists")
# def get_playlists():
#     return {"playlists": get_user_playlists()}


# @app.get("/top-artists/{timePeriod}")
# def get_top_artists(timePeriod: int):
#     return {"top-artists": get_user_top_artists(timePeriod)}


# @app.get("/top-tracks/{timePeriod}")
# def get_top_tracks(timePeriod: int):
#     return {"top-tracks": get_user_top_tracks(timePeriod)}


# @app.get("/top-genres/{timePeriod}")
# def get_top_genres(timePeriod: int):
#     return {"top-genres": get_user_top_genres(timePeriod)}


# @app.get("/check-cookie")
# def check_cookie(req: Request):
#     token = req.cookies.get("access_token")
#     return {"token": token}


# @app.get("/user-spotify-data")
# def user_info():
#     return {"user": get_user_data()}


# @app.get("/user-id")
# def get_id():
#     return {"id": get_user_id()}
