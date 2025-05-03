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
from fastapi import Request, Response
from collections import defaultdict

load_dotenv()


class Artist(BaseModel):
    name: str


client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8000/callback"  # temp
# redirect_uri = "http://localhost:3000/login"
scope = "user-read-private user-read-email playlist-read-private playlist-read-collaborative user-top-read"  # should move to a type file

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True,
    cache_path=".spotify_cache",
)

# temp var - should store in a cookie later
user_access_token = None

sp = Spotify(user_access_token)


def get_client():
    return client_id, client_secret


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    # query will use a comma delimited list for type
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        raise Exception("No artist found")
    return json_result[0]


def get_artist_id(token, artist_name):
    result = search_for_artist(token, artist_name)
    return result["id"]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    songs = []
    for i, song in enumerate(json_result):
        songs.append(song["name"])
    return songs


# Functiosn below are the acc useful ones for this project


# redirect the user to the spotify site to get perms
def login():
    auth_url = sp_oauth.get_authorize_url()
    # return RedirectResponse(auth_url)
    return auth_url


def get_spotify_client(token=None):
    if token:
        return Spotify(auth=token)
    return Spotify(auth=user_access_token)


# get the different tokens from spotify, should store the tokens in a cookie or something
async def callback_func(req: Request, res: Response):
    code = req.query_params.get("code")
    if not code:
        return JSONResponse(
            {"error": "Authorization code not provided"}, status_code=400
        )

    try:
        token_info = sp_oauth.get_access_token(code)
        if not token_info:
            return JSONResponse(
                {"error": "Failed to retrieve access token"}, status_code=500
            )

        # modify this to store tokens in a https cookie
        global user_access_token, sp
        user_access_token = token_info["access_token"]
        sp = Spotify(auth=user_access_token)

        frontend_url = "http://localhost:3000/login?auth=success"
        redirect_response = RedirectResponse(url=frontend_url)

        redirect_response.set_cookie(
            key="access_token",
            value=token_info["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
        )

        if "refresh_token" in token_info:
            redirect_response.set_cookie(
                key="refresh_token",
                value=token_info["refresh_token"],
                httponly=True,
                secure=False,
                samesite="lax",
                path="/",
            )

        return redirect_response

    except Exception as e:
        return JSONResponse({"error": f"An error occurred: {str(e)}"}, status_code=500)


def refresh_access_token(refresh_token: str):
    global user_access_token
    token_info = sp_oauth.refresh_access_token(refresh_token)
    user_access_token = token_info["access_token"]


def get_user_playlists():
    playlists = sp.current_user_playlists()
    res = []
    for playlist in playlists["items"]:
        res.append(playlist["name"])
    return res


# store this in a type file later
time_ranges = {1: "short_term", 2: "medium_term", 3: "long_term"}


def get_user_top_artists(time_range: int):
    top_artists = sp.current_user_top_artists(time_range=time_ranges[time_range])
    res = []
    for artist in top_artists["items"]:
        res.append(artist)
    return res


def get_user_top_tracks(time_range: int):
    top_tracks = sp.current_user_top_tracks(time_range=time_ranges[time_range])
    res = []
    for track in top_tracks["items"]:
        res.append(track["name"])
    return res


# returns a hashmap of genres and its "popularity" for the user, counts its frequency among the users favourite artists
def get_user_top_genres(time_range: int):
    top_artists = get_user_top_artists(time_range)
    res = defaultdict(int)
    for artist in top_artists:
        for genre in artist["genres"]:
            res[genre] += 1
    return res
