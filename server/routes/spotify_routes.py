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
def spotify_login():
    return login()


@router.get("/callback")
async def callback(request: Request, response: Response):
    return await callback_func(request, response)


@router.get("/user-data")
def get_user_data(req: Request, res: Response):
    sp = get_spotify_client(req, res)
    user_info = sp.current_user()
    return {
        "user" : user_info
    }


@router.get("/user-id")
def get_user_spotify_id(req: Request, res: Response):
    sp = get_spotify_client(req, res)
    user_info = sp.current_user()
    return user_info["id"]
