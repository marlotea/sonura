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
from fastapi import Request, Response, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
import time

load_dotenv()

httponly_flag_cookies = True
if os.getenv("ENVIRONMENT") == "dev":
    httponly_flag_cookies = False

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
scope = os.getenv("SPOTIFY_SCOPE")

def create_spotify_oauth():
    return SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True,
    cache_path=".spotify_cache",
)

# class for spotify service
class SpotifyService:
    def __init__(self, req: Request, res: Response):
        self.req = req
        self.res = res
        self.sp_oauth = create_spotify_oauth()
        self.sp = None
        
        self.time_ranges = {1: "short_term", 2: "medium_term", 3: "long_term"}

    def login(self):
        auth_url = self.sp_oauth.get_authorize_url()
        return RedirectResponse(auth_url)

    def callback(self):
        code = self.req.query_params.get("code")
        if not code:
            return JSONResponse({"error": "No authorization code provided"}, status_code=400)

        try:
            token_info = self.sp_oauth.get_access_token(code)
            if not token_info:
                return JSONResponse({"error": "Failed to get access token"}, status_code=500)

            self.res.set_cookie(key="access_token", value=token_info["access_token"], httponly=httponly_flag_cookies)
            self.res.set_cookie(key="refresh_token", value=token_info.get("refresh_token", ""), httponly=httponly_flag_cookies)
            self.res.set_cookie(key="expires_at", value=str(token_info["expires_at"]), httponly=httponly_flag_cookies)
            
            redirect_response = RedirectResponse("http://127.0.0.1:3000/login?auth=success")
            redirect_response.set_cookie(key="access_token", value=token_info["access_token"], httponly=httponly_flag_cookies)
            redirect_response.set_cookie(key="refresh_token", value=token_info.get("refresh_token", ""), httponly=httponly_flag_cookies)
            redirect_response.set_cookie(key="expires_at", value=str(token_info["expires_at"]), httponly=httponly_flag_cookies)

            self.sp = Spotify(auth=token_info["access_token"])

            return redirect_response

        except Exception as e:
            return JSONResponse({"error": f"Callback failed: {str(e)}"}, status_code=500)

    def get_client(self):
        access_token = self.req.cookies.get("access_token")
        refresh_token = self.req.cookies.get("refresh_token")
        expires_at = self.req.cookies.get("expires_at")

        if not access_token or not refresh_token or not expires_at:
            raise HTTPException(status_code=401, detail="Missing Tokens")

        if int(time.time()) >= int(expires_at):
            token_info = self.sp_oauth.refresh_access_token(refresh_token)
            access_token = token_info["access_token"]
            self.res.set_cookie(key="access_token", value=access_token, httponly=httponly_flag_cookies)
            self.res.set_cookie(key="expires_at", value=str(token_info["expires_at"]), httponly=httponly_flag_cookies)

        self.sp = Spotify(auth=access_token)
        return self.sp
    
    def get_user_playlists(self):
        if not self.sp:
            self.get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        playlists = self.sp.current_user_playlists()
        res = []
        for playlist in playlists["items"]:
            res.append(playlist["name"])
        return res
            
    def get_user_data(self):
        if not self.sp:
            self.get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        return self.sp.current_user()
    
    def get_user_top_artists(self, time_range: int):
        if not self.sp:
            self.get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_artists = self.sp.current_user_top_artists(time_range=self.time_ranges[time_range])
        res = []
        for artist in top_artists["items"]:
            res.append(artist)
        return res
    
    def get_user_top_tracks(self, time_range: int, limit: int):
        if not self.sp:
            self.get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_tracks = self.sp.current_user_top_tracks(time_range=self.time_ranges[time_range], limit=limit)
        res = []
        for track in top_tracks["items"]:
            res.append(track["name"])
        return res

    def get_user_top_genres(self, time_range: int):
        if not self.sp:
            self.get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_artists = self.get_user_top_artists(time_range)
        res: defaultdict[str, int] = defaultdict(int)
        for artist in top_artists:
            for genre in artist["genres"]:
                res[genre] += 1
        return res


# stuff from yt
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
