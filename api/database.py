from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite. 
# In a production environment, this would be a PostgreSQL or MySQL URL.
# For this MVP and academic defense, SQLite is sufficient and requires no external setup.
# Database URL for SQLite.
# Using in-memory database for Vercel ensuring no file-permission errors.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create the database engine.
# connect_args={"check_same_thread": False} is needed only for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models. All models will inherit from this.
Base = declarative_base()

# Dependency to get a database session for each request.
# This ensures the session is closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
