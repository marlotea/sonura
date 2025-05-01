from dotenv import load_dotenv
import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.UserModels import Base

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    print("Creating Tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Successfully Created Tables")
    except Exception as e:
        print(f"Failed to create tables: {e}")