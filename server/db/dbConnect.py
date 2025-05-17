from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.UserModels import Base

load_dotenv()

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