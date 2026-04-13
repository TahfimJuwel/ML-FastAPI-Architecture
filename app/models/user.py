from sqlalchemy import Column, Integer, String
from app.db.database import Base # import Base from db folder
from sqlalchemy.orm import relationship

class UserTable(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    logs = relationship("SentimentLogTable", back_populates="owner")