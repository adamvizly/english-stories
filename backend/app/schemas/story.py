from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class EnglishLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class GrammarNote(BaseModel):
    concept: str
    explanation: str
    examples: List[str]

class StoryBase(BaseModel):
    title: str
    content: str
    level: EnglishLevel
    topic: str

class StoryRequest(StoryBase):
    pass

class StoryResponse(StoryBase):
    id: int
    grammar_notes: List[GrammarNote]

    class Config:
        from_attributes = True
