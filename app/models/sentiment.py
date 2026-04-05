from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base # import Base from db folder

class SentimentLogTable(Base):
    __tablename__ = "sentiment_logs" 
    
    id = Column(Integer, primary_key=True)
    user_text = Column(String)
    score = Column(Float)
    sentiment_label = Column(String)