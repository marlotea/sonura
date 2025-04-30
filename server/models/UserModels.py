from pydantic import BaseModel

class Music_Profile(BaseModel):
    top_genre : str | None

class User(BaseModel):
    id: int | None
    username: str | None
    email : str | None
    passsword: str | None
    salt : str | None
    spotify_username : str | None
    music_profile : Music_Profile | None