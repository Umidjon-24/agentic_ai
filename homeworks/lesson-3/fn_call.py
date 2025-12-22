from google import genai
from google.genai import types
from sqlalchemy import create_engine, text, inspect
from typing import Any, Dict, List
import os
from dotenv import load_dotenv
load_dotenv('.env')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

engine = create_engine(
    "mssql+pyodbc://@DESKTOP-EQ1S466/sales"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

def list_tables() -> Dict[str, Any]:
    """List available tables in the connected database."""
    insp = inspect(engine)
    tables = sorted(insp.get_table_names())
    return {"tables": tables, "count": len(tables)}


def describe_table(table: str) -> Dict[str, Any]:
    """Describe columns for a given table name (exact match)."""
    insp = inspect(engine)
    if table not in insp.get_table_names():
        return {"error": f"Unknown table '{table}'.", "hint": "Call list_tables() first."}
    cols = insp.get_columns(table)
    columns = [
        {
            "name": c.get("name"),
            "type": str(c.get("type")),
            "nullable": bool(c.get("nullable", True)),
        }
        for c in cols
    ]
    return {"table": table, "columns": columns}


def tool_db(query: str) -> Dict[str, Any]:
    """Run read-only select SQL query
    Args:
        query
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
    
    if not rows:
        return "No results found."

    rows_list = [dict(row._mapping) for row in rows]
    return {"results": rows_list}

config = types.GenerateContentConfig(
    tools=[tool_db, describe_table, list_tables]
) 


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""
    What are the names of products?""",
    config=config,
)

print(response.text) 
