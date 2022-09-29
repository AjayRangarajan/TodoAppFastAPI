from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URI = os.getenv("DATABASE_URI")


engine = create_engine(DATABASE_URI)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)