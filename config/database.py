from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://username:password@localhost/mydatabase"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

# Function to create a new session
def get_session():
    return Session()

# Function to create the tables
def create_tables():
    from models import Base  # Import Base from your models
    Base.metadata.create_all(engine)
