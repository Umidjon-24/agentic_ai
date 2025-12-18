from google import genai
from google.genai import types
from sqlalchemy import create_engine, text, inspect
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv('.env')

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hi"
)

