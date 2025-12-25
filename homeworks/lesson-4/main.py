from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List
from sqlalchemy import create_engine, text, inspect
import pyodbc

mcp = FastMCP('demo')
engine = create_engine(
    "mssql+pyodbc://@DESKTOP-EQ1S466/sales"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    )

@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Adds two numbers and return result
    """
    return a + b

@mcp.tool()
def list_tables() -> Dict[str, Any]:
    
    """List available tables in the connected database."""
    insp = inspect(engine)
    tables = sorted(insp.get_table_names())
    return {"tables": tables, "count": len(tables)}

@mcp.tool()
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

@mcp.tool()
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


if __name__ == '__main__':
    print("Running...")
    mcp.run(transport='stdio')