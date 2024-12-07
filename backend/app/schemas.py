from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class EnglishLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class StoryBase(BaseModel):
    title: str
    content: str
    topic: str
    level: EnglishLevel

class StoryResponse(StoryBase):
    id: int

    class Config:
        from_attributes = True

class StoryRequest(BaseModel):
    topic: str
    level: EnglishLevel

class GrammarHintRequest(BaseModel):
    level: Optional[EnglishLevel] = None

class GrammarHint(BaseModel):
    title: str
    explanation: str
    examples: List[str]
    practice_exercises: List[str]
    level: EnglishLevel
