from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
import os
import sqlite3
import requests
from sqlalchemy.pool import StaticPool

def get_sql_database():
    url = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/main/src/create.sql"
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(requests.get(url).text)
    engine = create_engine("sqlite://", creator=lambda: connection, poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    return SQLDatabase(engine)