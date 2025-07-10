from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # FK to users table
    keyword = Column(String, nullable=False)
    source = Column(String, nullable=False)
    snippet = Column(String)
    link = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="new")
