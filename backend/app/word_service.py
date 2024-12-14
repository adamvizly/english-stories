from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.models.word import DailyWord
from app.schemas.word import WordRequest, WordResponse
from app.services.gemini_service import GeminiService

class WordService:
    def __init__(self, db: Session, gemini_service: Optional[GeminiService] = None):
        self.db = db
        self.gemini = gemini_service or GeminiService()

    def generate_word_with_ai(self, level: str = 'BEGINNER') -> WordResponse:
        """
        Generate a new word using Gemini AI based on the specified level
        """
        # Use Gemini to generate a word with its details
        word_details = self.gemini.generate_word_with_details(level)

        # Create the word in the database
        word_request = WordRequest(
            word=word_details['word'],
            persian_meaning=word_details['persian_meaning'],
            synonyms=word_details.get('synonyms', [])
        )
        
        return WordResponse(
            word=word_request.word,
            persian_meaning=word_request.persian_meaning,
            synonyms=word_request.synonyms
        )
