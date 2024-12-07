import google.generativeai as genai
import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from . import models
from .config import GEMINI_API_KEY
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
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

        story_prompt = f"""Generate a short story about {topic}. 
        The story should be suitable for {level} English learners, using {level_descriptions[level]}.
        The story should be engaging and include a clear beginning, middle, and end.
        Also generate an appropriate title for the story.
        Format: 
        Title: [Story Title]
        Story: [Story Content]
        """

        grammar_prompt = f"""Analyze the story and identify 3 key grammar concepts used.
        Return ONLY a JSON object with this exact structure:
        {{
            "grammar_notes": [
                {{
                    "concept": "Past Simple Tense",
                    "explanation": "Used to describe completed actions in the past",
                    "examples": [
                        "She walked to the store",
                        "He bought a new book"
                    ]
                }},
                {{
                    "concept": "Another Grammar Concept",
                    "explanation": "Brief explanation",
                    "examples": [
                        "Example 1",
                        "Example 2"
                    ]
                }},
                {{
                    "concept": "Third Grammar Concept",
                    "explanation": "Brief explanation",
                    "examples": [
                        "Example 1",
                        "Example 2"
                    ]
                }}
            ]
        }}
        Do not include any other text, only the JSON object."""

        try:
            # Generate story
            story_response = self.ai_model.generate_content(story_prompt)
            if not story_response.text:
                logger.error("Empty response from AI model for story")
                return None
            
            # Parse the story response
            story_text = story_response.text
            title_start = story_text.find("Title:") + 6
            story_start = story_text.find("Story:") + 6
            
            title = story_text[title_start:story_start].strip()
            content = story_text[story_start:].strip()

            # Generate grammar notes
            grammar_response = self.ai_model.generate_content(
                f"Story: {content}\n\n{grammar_prompt}"
            )
            
            if not grammar_response.text:
                logger.error("Empty response from AI model for grammar notes")
                grammar_notes = []
            else:
                try:
                    # Clean up the response text to ensure it's valid JSON
                    grammar_text = grammar_response.text.strip()
                    if grammar_text.startswith('```json'):
                        grammar_text = grammar_text[7:]
                    if grammar_text.endswith('```'):
                        grammar_text = grammar_text[:-3]
                    grammar_text = grammar_text.strip()
                    
                    grammar_data = json.loads(grammar_text)
                    grammar_notes = grammar_data.get("grammar_notes", [])
                    
                    # Validate the structure of grammar notes
                    for note in grammar_notes:
                        if not all(key in note for key in ["concept", "explanation", "examples"]):
                            logger.error("Invalid grammar note structure")
                            grammar_notes = []
                            break
                        if not isinstance(note["examples"], list) or len(note["examples"]) < 2:
                            logger.error("Invalid examples in grammar note")
                            grammar_notes = []
                            break
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing grammar notes JSON: {str(e)}")
                    grammar_notes = []
                except Exception as e:
                    logger.error(f"Unexpected error processing grammar notes: {str(e)}")
                    grammar_notes = []

            # Create and save the story
            story = models.Story(
                title=title,
                content=content,
                topic=topic,
                level=level,
                grammar_notes=grammar_notes
            )
            db.add(story)
            db.commit()
            db.refresh(story)
            return story

        except Exception as e:
            db.rollback()
            logger.error(f"Error generating story: {str(e)}")
            return None
