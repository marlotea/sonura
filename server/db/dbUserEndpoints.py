from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
import bcrypt

from ..models.UserModels import User

DB_URL = os.getenv("DB_URL")

# def create_user(user : User):
#     try:
#         conn = 


