from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class DailyWord(Base):
    __tablename__ = "daily_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    persian_meaning = Column(String, nullable=False)
    synonyms = Column(JSON, nullable=True)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())
