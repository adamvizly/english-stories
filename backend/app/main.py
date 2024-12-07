from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app.routers import auth
from app.database import Base, engine, SessionLocal, get_db
from app.models import Story, User  # This ensures all models are loaded
from app.story_service import StoryService
from app.schemas import StoryRequest, StoryResponse
from app.schemas.story import EnglishLevel
from app.utils.auth import get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning Stories API")

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173"   # Vite preview
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
