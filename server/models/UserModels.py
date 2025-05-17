from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

Base = declarative_base()

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True)
    spotify_display_name = Column(String)
    spotify_refresh_token = Column(String)

    songs = relationship("UserSong", back_populates="user", cascade="all, delete-orphan")


    
class UserSong(Base):
    __tablename__ = "user_songs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.spotify_id"))
    song_id = Column(String, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="songs")
    __table_args__ = (UniqueConstraint("user_id", "song_id", name="user_song_unique"),)

    
    