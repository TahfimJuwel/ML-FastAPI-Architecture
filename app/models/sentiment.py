from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base # import Base from db folder

class SentimentLogTable(Base):
    __tablename__ = "sentiment_logs" 
    
    id = Column(Integer, primary_key=True)
    user_text = Column(String)
    score = Column(Float)
    sentiment_label = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserTable", back_populates="logs")
    