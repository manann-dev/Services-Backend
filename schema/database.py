from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .base import Base  # Import the Base you have defined
import os 

DATABASE_URI = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URI, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
