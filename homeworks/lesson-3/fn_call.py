from google import genai
from google.genai import types
from sqlalchemy import create_engine, text, inspect
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv('.env')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

engine = create_engine(
    "mssql+pyodbc://@DESKTOP-EQ1S466/sales"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

def tool_db(query: str):
    """Run SQL query.
    Args:
        query
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
    if not rows:
        return "No results found."

    return [dict(row._mapping) for row in rows]

config = types.GenerateContentConfig(
    tools=[tool_db]
)  # Pass the function itself

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""
    What are the names of customers?""",
    config=config,
)

print(response.text) 
