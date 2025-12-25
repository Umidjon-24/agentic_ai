from google import genai
from google.genai import types
import pyodbc
import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv('.env')

class DB:
    def __init__ (self):
        connection_string = (
    "mssql+pyodbc://@DESKTOP-EQ1S466/chatbot_db"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    )
        self.cur = create_engine(connection_string)

    def register(self, username, password):
        pass

    def login(self, username, password):
        pass

    def load_history(self, user_id):
        pass

    def save_message(self, user_id, message, role):
        pass

class Agent:
    def __init__ (self, user_id):
        pass

    def ask(self):
        pass

class Application:
    def __init__ (self):
        self.commands = {
            0: self.show_0menu,
            1: self.register,
            2: self.login,
            3: sys.exit}
        
        self.menu = """Menu:
0. Menu
1. Registration
2. Login
3. Exit"""
    
    def show_menu(self):
        print(self.menu)
    
    def register(self):
        print("Register")

    def login(self):
        print("Login")

    def run(self):
        self.show_menu()
        while True:
            command_id = input("Command ID:")
            command_id = int(command_id)
            command = self.commands[command_id]
            command()

app = Application()
app.run()

        
    


