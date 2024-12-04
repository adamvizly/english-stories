from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List
import os
from dotenv import load_dotenv
from .database import SessionLocal, engine, Base
from .models import Story
from .story_service import StoryService

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning Stories API")

class EnglishLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class StoryRequest(BaseModel):
    topic: str
    level: EnglishLevel

class StoryResponse(BaseModel):
    title: str
    content: str
    topic: str
    level: EnglishLevel

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/stories/", response_model=StoryResponse)
async def get_story(request: StoryRequest):
    """
    Get a story based on topic and English proficiency level.
    First checks the database for existing stories, if none found, generates a new one.
    """
    db = next(get_db())
    story_service = StoryService()
    
    # First try to find an existing story
    story = story_service.find_story(db, request.topic, request.level)
    
    if not story:
        # Generate a new story if none exists
        story = story_service.generate_story(db, request.topic, request.level)
        if not story:
            raise HTTPException(status_code=500, detail="Failed to generate story")
    
    return StoryResponse(
        title=story.title,
        content=story.content,
        topic=story.topic,
        level=story.level
    )

@app.get("/stories/", response_model=List[StoryResponse])
async def list_stories(topic: str = None, level: EnglishLevel = None):
    """
    List all stories, optionally filtered by topic and/or level
    """
    db = next(get_db())
    story_service = StoryService()
    stories = story_service.list_stories(db, topic, level)
    
    return [
        StoryResponse(
            title=story.title,
            content=story.content,
            topic=story.topic,
            level=story.level
        )
        for story in stories
    ]
