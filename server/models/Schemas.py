from pydantic import BaseModel
from typing import Optional

class MusicProfileSchema(BaseModel):
    top_genres : Optional[str] = None
    top_artists : Optional[str] = None
    
class UserCreateSchema(BaseModel):
    username: str
    password: str
    salt: str
    spotify_username: str
    music_profile: MusicProfileSchema
    
class UserResponseSchema(UserCreateSchema):
    id: int