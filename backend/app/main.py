from ast import Str
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from app.routers import auth
from app.database import Base, engine, SessionLocal, get_db
from app.models import Story, User  # This ensures all models are loaded
from app.story_service import StoryService
from app.word_service import WordService
from app.schemas import StoryRequest, StoryResponse
from app.schemas.story import EnglishLevel
from app.utils.auth import get_current_user
from app.schemas.story import EnglishLevel

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning Stories API")

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview
    "http://localhost:80",    # Production frontend
    "http://localhost"        # Production frontend (alternative)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)  

story_service = StoryService()
word_service = WordService()

@app.post("/stories/", response_model=StoryResponse)
async def create_story(
    request: StoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a new story based on the provided topic and level.
    The story will be newly generated each time using AI.
    Requires authentication.
    """
    story = story_service.generate_story(db, request.topic, request.level.value)
    if not story:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate story"
        )
    
    return story

@app.get("/stories/", response_model=List[StoryResponse])
async def list_stories(
    topic: Optional[str] = Query(None, description="Filter stories by topic"),
    level: Optional[EnglishLevel] = Query(None, description="Filter stories by English level"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all stories with optional filtering by topic and level.
    Requires authentication.
    """
    stories = story_service.list_stories(db, topic, level.value if level else None)
    return stories

@app.get("/daily-words/")
async def get_daily_words(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get daily words for the current user.
    If words haven't been generated for today, generates new ones.
    """
    return word_service.get_daily_words(db, current_user)
