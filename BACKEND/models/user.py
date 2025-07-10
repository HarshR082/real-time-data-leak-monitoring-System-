from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship  # <-- import relationship here
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    keywords = relationship("Keyword", back_populates="user")  # Fix indentation and case
