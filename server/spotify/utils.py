from dotenv import load_dotenv
import os
import base64
from requests import post
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request, Response, HTTPException
from collections import defaultdict
import time

# our modules
from models.UserModels import User, UserSong
from db.utils import create_new_user, query_user, user_exists, query_user_refresh_token, add_user_songs, add_song, delete_all_user_songs

load_dotenv()

# env variables
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
        # return auth_url
        return RedirectResponse(auth_url)

    def callback(self):
        code = self.req.query_params.get("code")
        if not code:
            return JSONResponse({"error": "No authorization code provided"}, status_code=400)

        try:
            token_info = self.sp_oauth.get_access_token(code)
            if not token_info:
                return JSONResponse({"error": "Failed to get access token"}, status_code=500)
            
            access_token = token_info["access_token"]
            expires_at = token_info["expires_at"]
            refresh_token = token_info["refresh_token"]
            
            redirect_response = RedirectResponse("http://127.0.0.1:3000/dashboard")
            self.sp = Spotify(auth=token_info["access_token"])
            
            sp_user_id = self.sp.current_user()["id"]
            sp_user_display_name = self.sp.current_user()["display_name"]
            if not user_exists(sp_user_id):
                create_new_user(sp_user_id, sp_user_display_name, refresh_token)
                
            self.req.session["spotify_id"] = sp_user_id
            self.req.session["access_token"] = access_token
            self.req.session["expires_at"] = expires_at
            
            delete_all_user_songs(sp_user_id)
            self._add_songs_to_db()
            
            return redirect_response

        except Exception as e:
            return JSONResponse({"error": f"Callback failed: {str(e)}"}, status_code=500)

    def get_user_playlists(self):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        playlists = self.sp.current_user_playlists()
        res = {}
        for playlist in playlists["items"]:
            res[playlist["name"]] = playlist["id"]
        return res
            
    def get_user_data(self):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        return self.sp.current_user()
    
    def get_user_top_artists(self, time_range: int):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_artists = self.sp.current_user_top_artists(time_range=self.time_ranges[time_range])
        res = []
        for artist in top_artists["items"]:
            res.append(artist)
        return res
    
    def get_user_top_tracks(self, time_range: int, limit: int):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_tracks = self.sp.current_user_top_tracks(time_range=self.time_ranges[time_range], limit=limit)
        return top_tracks

    def get_user_top_genres(self, time_range: int):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        top_artists = self.get_user_top_artists(time_range)
        res: defaultdict[str, int] = defaultdict(int)
        for artist in top_artists:
            for genre in artist["genres"]:
                res[genre] += 1
        return res
    
    def create_playlist(self):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        
        user_id = self.sp.me()["id"]
        
        # check if the sonura playlist already exists
        playlist_name, playlist_id = self._get_sonura_playlist()
        if playlist_name and playlist_id:
            return "Sonura playlist already exists"
        
        self.sp.user_playlist_create(
            user=user_id,
            name="Sonura",
            public=True,
            description="Created with Sonura"
        )
        
        return "Successfully created Sonura Playlist"
    
    def add_to_playlist(self, track_uri: str):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        
        playlist_name, playlist_id = self._get_sonura_playlist()
        if not playlist_name or not playlist_id:
            self.create_playlist()
        
        self.sp.playlist_add_items(playlist_id=playlist_id, items=[self._get_track_uri(track_uri)])
        return f"Successfully added track {track_uri} to Sonura playlist"
    
    def _get_client(self):
        access_token = self.req.session.get("access_token")
        expires_at = self.req.session.get("expires_at")
        sp_user_id = self.req.session.get("spotify_id")
        
        if not sp_user_id:
            raise HTTPException(status_code=401, detail="No Spotify ID in session")

        if not access_token or not expires_at:
            raise HTTPException(status_code=401, detail="Missing Tokens")

        if int(time.time()) >= int(expires_at):
            refresh_token = self._get_new_access_token(sp_user_id)
            token_info = self.sp_oauth.refresh_access_token(refresh_token)
            access_token = token_info["access_token"]
            self.req.session["access_token"] = access_token
            self.req.session["expires_at"] = expires_at

        self.sp = Spotify(auth=access_token)
        return self.sp
    
    def _add_songs_to_db(self):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        try:
            top_tracks = self.get_user_top_tracks(2, 50)
            top_tracks_ids = []
            for track in top_tracks["items"]:
                top_tracks_ids.append(track["id"])
            add_user_songs(self.req.session.get("spotify_id"), top_tracks_ids)
            return {
                "message" : "Successfully added songs to db"
            }
        except Exception as e:
            return JSONResponse({"error": f"Adding to db failed: {str(e)}"}, status_code=400)
        
    
    def _get_new_access_token(self, spotify_id):
        refresh_token = query_user_refresh_token(spotify_id)
        return refresh_token
    
    def _get_sonura_playlist(self):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        
        playlists = self.get_user_playlists()
        for key, value in playlists.items():
            if key == "Sonura":
                return key, value
        return None, None
    
    def _get_track_uri(self, track_name: str):
        if not self.sp:
            self._get_client()
        if not self.sp:
            raise HTTPException(status_code=500, detail="Spotify client initialization failed")
        
        results = self.sp.search(q=track_name, type="track", limit=1)
        tracks = results["tracks"]["items"]
        if tracks:
            return tracks[0]["uri"]
        return None