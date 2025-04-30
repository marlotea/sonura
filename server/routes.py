import dotenv
from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os
import psycopg2

from .db.dbConnect import conn

cur = conn.cursor()

async def check_version():
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"Version: {version}")
