import os

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DBModel(Base):
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    accuracy = Column(Float)
    is_deployed = Column(Boolean)

Base.metadata.create_all(bind=engine)


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_logs" 
    
    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String)
    score = Column(Float)
    sentiment_label = Column(String) 

# DEEP DIVE: What happens when you run this?
# SQLAlchemy checks Postgres. It sees "ml_models" already exists, so it skips it.
# It sees "sentiment_logs" DOES NOT exist, so it runs a CREATE TABLE command to build it!
Base.metadata.create_all(bind=engine)