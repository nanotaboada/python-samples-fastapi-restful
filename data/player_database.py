# -------------------------------------------------------------------------------------------------
# Database
# -------------------------------------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./data/players-sqlite3.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
OrmSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
