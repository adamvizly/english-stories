from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.word import DailyWord
from app.services.gemini_service import GeminiService

class WordService:
    def __init__(self):
        self.gemini = GeminiService()

    def get_daily_words(self, db: Session) -> List[Dict]:
        """
        Generate daily words without user-specific context.
        
        Args:
            db (Session): Database session
        
        Returns:
            List of dictionaries containing word details
        """
        # Check if words already exist for today
        today = datetime.now().date()
        existing_words = (
            db.query(DailyWord)
            .filter(DailyWord.created_at >= today)
            .all()
        )
        
        if existing_words:
            return [
                {
                    "word": word.word, 
                    "persian_meaning": word.persian_meaning,
                    "synonyms": word.synonyms
                } 
                for word in existing_words
            ]
            
        # Generate new words using Gemini for a default level
        try:
            word_data_list = self.gemini.generate_words("INTERMEDIATE")
        except Exception as e:
            print(f"Error generating words: {e}")
            return []
        
        new_words = []
        for word_data in word_data_list:
            daily_word = DailyWord(
                word=word_data.get('word', ''),
                persian_meaning=word_data.get('persian_meaning', ''),
                synonyms=word_data.get('synonyms', [])
            )
            db.add(daily_word)
            new_words.append(daily_word)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error saving daily words: {e}")
            return []
        
        return [
            {
                "word": word.word, 
                "persian_meaning": word.persian_meaning,
                "synonyms": word.synonyms
            } 
            for word in new_words
        ]
