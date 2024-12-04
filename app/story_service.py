from sqlalchemy.orm import Session
from . import models
import google.generativeai as genai
import os
import logging
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.ai_model = genai.GenerativeModel("gemini-1.5-flash")

    def find_story(self, db: Session, topic: str, level: str) -> Optional[models.Story]:
        """Find an existing story in the database"""
        return db.query(models.Story).filter(
            models.Story.topic == topic,
            models.Story.level == level
        ).first()

    def list_stories(
        self, 
        db: Session, 
        topic: Optional[str] = None, 
        level: Optional[str] = None
    ) -> List[models.Story]:
        """List stories with optional filtering"""
        query = db.query(models.Story)
        if topic:
            query = query.filter(models.Story.topic == topic)
        if level:
            query = query.filter(models.Story.level == level)
        return query.all()

    def generate_story(self, db: Session, topic: str, level: str) -> Optional[models.Story]:
        """Generate a new story using Gemini"""

        # Craft prompt based on level
        level_descriptions = {
            "beginner": "simple vocabulary and basic sentence structures",
            "intermediate": "moderate vocabulary and compound sentences",
            "advanced": "rich vocabulary, complex sentences, and idiomatic expressions"
        }

        prompt = f"""Generate a short story about {topic}. 
        The story should be suitable for {level} English learners, using {level_descriptions[level]}.
        The story should be engaging and include a clear beginning, middle, and end.
        Also generate an appropriate title for the story.
        Format: 
        Title: [Story Title]
        Story: [Story Content]
        """

        try:
            completion = self.ai_model.generate_content(prompt)
            
            # Parse the response to extract title and content
            story_text = completion.text
            title_start = story_text.find("Title:") + 6
            story_start = story_text.find("Story:") + 6
            
            title = story_text[title_start:story_start].strip()
            content = story_text[story_start:].strip()

            # Create and save the story
            story = models.Story(
                title=title,
                content=content,
                topic=topic,
                level=level
            )
            db.add(story)
            db.commit()
            db.refresh(story)
            return story

        except Exception as e:
            db.rollback()
            print(f"Error generating story: {str(e)}")
            return None
