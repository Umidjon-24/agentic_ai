from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import get_db
from db import User

connection_string = (
    "mssql+pyodbc://@DESKTOP-EQ1S466/chatbot_db"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
engine = create_engine(connection_string)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    session = next(get_db())
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_message_id = Column(Integer)
    message = Column(Text)
    role = Column(String(50)) 

Base.metadata.create_all(engine)

print("Tables created successfully!")