from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from pydantic import BaseModel
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request, Response, APIRouter
from collections import defaultdict

from spotify.utils import *

load_dotenv()

router = APIRouter()


@router.get("/login")
async def spotify_login(req: Request):
    spotify = SpotifyService(req, Response())
    return spotify.login()


@router.get("/callback")
async def callback(req: Request, res: Response):
    spotify = SpotifyService(req, res)
    return spotify.callback()


@router.get("/user-data")
def get_user_spotify_data(req: Request, res: Response):
    spotify = SpotifyService(req, res)
    sp_client = spotify.get_client()
    user_info = get_user_data(sp_client)
    return {
        "user" : user_info
    }


@router.get("/user-id")
def get_user_spotify_id(req: Request, res: Response):
    sp = get_spotify_client(req, res)
    user_info = get_user_data(sp)
    return user_info["id"]

@router.get("/top-artists/{timePeriod}")
def get_top_artists(req: Request, res: Response, timePeriod: int):
    sp = get_spotify_client(req, res)
    return {"top-artists": get_user_top_artists(sp, timePeriod)}


@router.get("/top-tracks/{timePeriod}/{limit}")
def get_top_tracks(req: Request, res: Response, timePeriod: int, limit: int):
    sp = get_spotify_client(req, res)
    return {"top-tracks": get_user_top_tracks(sp, timePeriod, limit)}


@router.get("/top-genres/{timePeriod}")
def get_top_genres(req: Request, res: Response, timePeriod: int):
    sp = get_spotify_client(req, res)
    return {"top-genres": get_user_top_genres(sp, timePeriod)}