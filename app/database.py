from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# create a database url
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

# create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# start a session
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for db and ORM models
Base = declarative_base()

# Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()