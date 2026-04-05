from sqlalchemy import Column, Integer, String
from app.db.database import Base # import Base from db folder

class UserTable(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)