from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.models.word import DailyWord
from app.models.auth import User
from app.services.gemini_service import GeminiService

# This is a mock word database - in production, you would want to use a real dictionary API
WORD_DATABASE = {
    'BEGINNER': [
        {'word': 'happy', 'persian': 'خوشحال', 'synonyms': ['joyful', 'glad']},
        {'word': 'sad', 'persian': 'غمگین', 'synonyms': ['unhappy', 'sorrowful']},
        # Add more words...
    ],
    'INTERMEDIATE': [
        {'word': 'perseverance', 'persian': 'پشتکار', 'synonyms': ['persistence', 'determination']},
        {'word': 'eloquent', 'persian': 'فصیح', 'synonyms': ['articulate', 'fluent']},
        # Add more words...
    ],
    'ADVANCED': [
        {'word': 'ephemeral', 'persian': 'زودگذر', 'synonyms': ['transient', 'fleeting']},
        {'word': 'ubiquitous', 'persian': 'همه‌جا حاضر', 'synonyms': ['omnipresent', 'universal']},
        # Add more words...
    ]
}

class WordService:
    def __init__(self):
        self.gemini = GeminiService()

    def get_daily_words(self, db: Session, user: User) -> List[DailyWord]:
        """Get or generate daily words for a user."""
        # Check if user already has words for today
        today = datetime.now().date()
        existing_words = (
            db.query(DailyWord)
            .filter(DailyWord.user_id == user.id)
            .filter(DailyWord.created_at >= today)
            .all()
        )
        
        if existing_words:
            return existing_words
            
        # Generate new words using Gemini
        word_data_list = self.gemini.generate_words(user.english_level.value)
        
        new_words = []
        for word_data in word_data_list:
            daily_word = DailyWord(
                user_id=user.id,
                word=word_data['word'],
                persian_meaning=word_data['persian'],
                synonyms=word_data['synonyms']
            )
            db.add(daily_word)
            new_words.append(daily_word)
            
        db.commit()
        return new_words
