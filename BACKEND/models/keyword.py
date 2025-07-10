from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.user import User  # okay if your import paths are correct

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="keywords")
