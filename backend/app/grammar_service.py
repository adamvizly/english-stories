import google.generativeai as genai
import logging
from typing import Optional
from .config import GEMINI_API_KEY
from .schemas import EnglishLevel, GrammarHint

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GrammarService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.ai_model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_grammar_hint(self, level: EnglishLevel) -> Optional[GrammarHint]:
        """Generate a grammar hint based on the English level"""
        
        level_descriptions = {
            EnglishLevel.BEGINNER: "basic grammar concepts, simple tenses, and everyday vocabulary",
            EnglishLevel.INTERMEDIATE: "intermediate grammar structures, compound sentences, and phrasal verbs",
            EnglishLevel.ADVANCED: "advanced grammar patterns, complex tenses, idiomatic expressions, and academic writing"
        }

        prompt = f"""Generate a new and unique English grammar lesson for {level.value} level students.
        Focus on {level_descriptions[level]}.
        
        Structure the response in JSON format with these fields:
        - title: A specific grammar point or rule
        - explanation: Clear explanation of the grammar rule
        - examples: List of 3 practical example sentences
        - practice_exercises: List of 3 fill-in-the-blank or rewrite exercises
        - level: The input level
        
        Make it engaging and practical for real-world usage."""

        try:
            response = self.ai_model.generate_content(prompt)
            if not response.text:
                logger.error("Empty response from AI model")
                return None

            # Parse the response into structured data
            import json
            hint_data = json.loads(response.text)
            
            return GrammarHint(
                title=hint_data["title"],
                explanation=hint_data["explanation"],
                examples=hint_data["examples"],
                practice_exercises=hint_data["practice_exercises"],
                level=level
            )

        except Exception as e:
            logger.error(f"Error generating grammar hint: {str(e)}")
            return None
