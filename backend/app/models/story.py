from sqlalchemy import Column, Integer, String, JSON, Enum
from app.database import Base
from app.schemas.story import EnglishLevel

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    level = Column(Enum(EnglishLevel))
    topic = Column(String)
    grammar_notes = Column(JSON)
