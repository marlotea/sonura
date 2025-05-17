from dotenv import load_dotenv
load_dotenv()
import os

from ..models.UserModels import User, UserSong

DB_URL = os.getenv("DB_URL")

async def create_user(user : User):
    pass

async def delete_user(id: int):
    pass

async def get_user_by_id(id: int):
    pass

async def get_user_by_username(username: str):
    pass

# add paramters later
async def update_user():
    pass
    


