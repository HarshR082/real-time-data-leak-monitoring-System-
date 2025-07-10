from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime

class LeakEvent(Base):
    __tablename__ = "leak_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # e.g., Low, Medium, High
    created_at = Column(DateTime, default=datetime.utcnow)
