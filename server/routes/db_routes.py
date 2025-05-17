from dotenv import load_dotenv
from fastapi import Request, Response, APIRouter
from pydantic import BaseModel

from ..models.Schemas import UserCreateSchema, UserResponseSchema, MusicProfileSchema
from ..models.UserModels import Music_Profile, User
from ..db.utils import hash, check_password
from ..db.dbConnect import Session_Local, engine, create_tables

load_dotenv()

router = APIRouter()