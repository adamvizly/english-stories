from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Story
from app.schemas import StoryRequest, StoryResponse
from app.schemas.story import GrammarNote, EnglishLevel
from app.services.gemini_service import GeminiService

class StoryService:
    def __init__(self):
        self.gemini = GeminiService()

    def create_story(self, db: Session, request: StoryRequest) -> StoryResponse:
        """
        Create a new story based on the request.

        Args:
            db (Session): Database session
            request (StoryRequest): Story creation request

        Returns:
            StoryResponse: Generated story
        """
        # Generate grammar notes using Gemini service
        story_content, grammar_notes = self.gemini.generate_story_with_grammar_notes(request.topic, request.level)

        # Create story model
        story_model = Story(
            title=request.topic,
            content=story_content,
            level=request.level,
            topic=request.topic,
            grammar_notes=grammar_notes
        )
        
        # Add to database
        db.add(story_model)
        db.commit()
        db.refresh(story_model)
        
        # Prepare response
        return StoryResponse(
            title=str(story_model.title),
            content=str(story_model.content),
            level=EnglishLevel(story_model.level),
            topic=str(story_model.topic),
            grammar_notes=[
                GrammarNote(
                    concept=note.get('concept', ''),
                    explanation=note.get('explanation', ''),
                    examples=note.get('examples', [])
                ) 
                for note in grammar_notes
            ]
        )

    def list_stories(
        self, 
        db: Session, 
        topic: Optional[str] = None, 
        level: Optional[str] = None
    ) -> List[StoryResponse]:
        """
        List stories with optional filtering.
        
        Args:
            db (Session): Database session
            topic (Optional[str]): Filter by topic
            level (Optional[str]): Filter by English level
        
        Returns:
            List[StoryResponse]: List of stories
        """
        query = db.query(Story)
        
        if topic is not None:
            query = query.filter(Story.topic == topic)
        
        if level is not None:
            query = query.filter(Story.level == level)
        
        stories = query.all()
        
        return [
            StoryResponse(
                title=str(story.title),
                content=str(story.content),
                level=EnglishLevel(story.level),
                topic=str(story.topic),
                grammar_notes=[
                    GrammarNote(
                        concept=note.get('concept', ''),
                        explanation=note.get('explanation', ''),
                        examples=note.get('examples', [])
                    ) 
                    for note in (story.grammar_notes or [])
                ]
            ) for story in stories
        ]
