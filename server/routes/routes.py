import dotenv
from typing import Union, Annotated
from fastapi import FastAPI, Header
import requests as req
import os
import psycopg2
from sqlalchemy import text

from db.dbConnect import Session_Local, engine

async def check_version():
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        db_name = conn.execute(text("SELECT current_database();")).scalar()
        return {
            "database" : db_name,
            "version" : version
        }