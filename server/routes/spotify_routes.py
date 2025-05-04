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
    user_info = spotify.get_user_data()
    return {
        "user" : user_info
    }


@router.get("/user-id")
def get_user_spotify_id(req: Request, res: Response):
    spotify = SpotifyService(req, res)
    user_info = spotify.get_user_data()
    return user_info["id"]

@router.get("/top-artists/{timePeriod}")
def get_top_artists(req: Request, res: Response, timePeriod: int):
    spotify = SpotifyService(req, res)
    return {"top-artists": spotify.get_user_top_artists(timePeriod)}


@router.get("/top-tracks/{timePeriod}/{limit}")
def get_top_tracks(req: Request, res: Response, timePeriod: int, limit: int):
    spotify = SpotifyService(req, res)
    return {"top-tracks": spotify.get_user_top_tracks(timePeriod, limit)}


@router.get("/top-genres/{timePeriod}")
def get_top_genres(req: Request, res: Response, timePeriod: int):
    spotify = SpotifyService(req, res)
    return {"top-genres": spotify.get_user_top_genres(timePeriod)}