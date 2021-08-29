# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///./data/songs.db", connect_args={"check_same_thread": False})
OrmSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
