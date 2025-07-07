from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL — file will be created next to your project
SQLALCHEMY_DATABASE_URL = "sqlite:///./decongito.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# initialize tables
def init_db():
    from app.models import ScanHistory
    Base.metadata.create_all(bind=engine)
