from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
