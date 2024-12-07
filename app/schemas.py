from pydantic import BaseModel
from enum import Enum
from typing import Optional

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
