from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
import sqlite3
import requests
from sqlalchemy.pool import StaticPool
import pandas as pd

def get_sql_database():
    url = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/main/src/create.sql"
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(requests.get(url).text)
    engine = create_engine("sqlite://", creator=lambda: connection, poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    return SQLDatabase(engine),connection

sql_db, raw_conn = get_sql_database()

def query_sqlite(query: str) -> str:
    """Executes a SQL query on the SQLite Northwind database and returns CSV"""
    try:
        df = pd.read_sql_query(query, raw_conn)
        return df.to_csv(index=False)
    except Exception as e:
        return f"Error: {str(e)}"

db_schema = sql_db.get_table_info()

