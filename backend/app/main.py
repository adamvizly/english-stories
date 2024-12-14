from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict

from app.database import Base, engine, get_db
from app.models import Story  # This ensures all models are loaded
from app.story_service import StoryService
from app.word_service import WordService
from app.schemas import StoryRequest, StoryResponse
from app.schemas.story import EnglishLevel
from app.schemas.word import WordRequest, WordResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning Stories API")

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview
    "http://localhost:80",    # Production frontend
    "http://localhost",        # Production frontend (alternative)
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

story_service = StoryService()
word_service = WordService(next(get_db()))

@app.post("/stories/", response_model=StoryResponse)
async def create_story(
    request: StoryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new story based on the provided topic and level.
    The story will be newly generated each time using AI.
    """
    return story_service.create_story(db, request)

@app.get("/stories/", response_model=List[StoryResponse])
async def list_stories(
    topic: Optional[str] = Query(None, description="Filter stories by topic"),
    level: Optional[str] = Query(None, description="Filter stories by English level"),
    db: Session = Depends(get_db)
):
    """
    List stories with optional filtering by topic and level.
    """
    return story_service.list_stories(db, topic, level)

@app.post("/words/")
async def create_word(
    word_request: WordRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new word manually.
    """
    return word_service.create_word(word_request)

@app.post("/words/generate", response_model=WordResponse)
async def generate_ai_word(
    level: str = Query(default='BEGINNER', enum=['BEGINNER', 'INTERMEDIATE', 'ADVANCED']),
    db: Session = Depends(get_db)
):
    """
    Generate a new word using Gemini AI
    """
    word_service = WordService(db)
    return word_service.generate_word_with_ai(level)

@app.get("/")
def read_root():
    return {"message": "Welcome to English Stories API"}
