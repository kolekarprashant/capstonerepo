from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
import sqlite3
import requests
from sqlalchemy.pool import StaticPool
import pandas as pd
from autogen import ConversableAgent, register_function
from config.llm_config import azure_openai_llm_config
# from API.tools.db_utils import query_sqlite,db_schema

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


def database_specialist_system_message(schema: str):
    return f"You are a database expert. Use your knowledge of the schema: {schema} to execute queries."


database_specialist = ConversableAgent(
    name="DatabaseSpecialist",
    system_message=database_specialist_system_message(db_schema),
    llm_config=azure_openai_llm_config,
    human_input_mode="NEVER",
)

register_function(
    query_sqlite,
    caller=database_specialist,
    executor=database_specialist,
    description="Executes a SQL query on the SQLite Northwind database and returns the result as CSV."
)
