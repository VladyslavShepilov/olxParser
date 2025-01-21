from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

import os
import dotenv

dotenv.load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def create_tables():
    Base.metadata.create_all(engine)
