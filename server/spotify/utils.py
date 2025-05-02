from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


class Artist(BaseModel):
    name: str


client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8000"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read",
    )
)


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


async def get_user_playlist():
    playlists = sp.current_user_playlists()
    res = []
    for playlist in playlists["items"]:
        res.append(playlist["name"])
    return res
