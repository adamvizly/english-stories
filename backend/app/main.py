from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal, engine, Base, get_db
from .models import Story, User
from .story_service import StoryService
from .grammar_service import GrammarService
from .schemas import StoryRequest, StoryResponse, EnglishLevel, GrammarHintRequest, GrammarHint
from auth.routes import router as auth_router
from auth.utils import get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning Stories API")
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

story_service = StoryService()
grammar_service = GrammarService()

@app.post("/stories/", response_model=StoryResponse)
async def get_story(
    request: StoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a story based on topic and English proficiency level.
    First checks the database for existing stories, if none found, generates a new one.
    Requires authentication.
    """
    # First try to find an existing story
    story = story_service.find_story(db, request.topic, request.level)
    
    # If no story exists, generate a new one
    if not story:
        story = story_service.generate_story(db, request.topic, request.level)
        if not story:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate story"
            )
    
    return story

@app.get("/stories/", response_model=List[StoryResponse])
async def list_stories(
    topic: str = None,
    level: EnglishLevel = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all stories, optionally filtered by topic and/or level.
    Requires authentication.
    """
    stories = story_service.list_stories(db, topic, level)
    
    return stories

@app.post("/grammar/hint/", response_model=GrammarHint)
async def get_grammar_hint(
    request: GrammarHintRequest = GrammarHintRequest(),
    current_user: User = Depends(get_current_user)
):
    """
    Get a personalized grammar hint based on the user's English level or requested level.
    The hint will be newly generated each time using AI.
    Requires authentication.
    """
    # Use requested level if provided, otherwise use user's level
    level = request.level or EnglishLevel.INTERMEDIATE  # You can add a level field to User model later
    
    hint = grammar_service.generate_grammar_hint(level)
    if not hint:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate grammar hint"
        )
    
    return hint
