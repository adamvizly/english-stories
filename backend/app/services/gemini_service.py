import google.generativeai as genai
from typing import List, Dict
import json
import os

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_words(self, level: str, count: int = 5) -> List[Dict]:
        """
        Generate words with their Persian meanings and synonyms using Gemini.
        
        Args:
            level: English proficiency level (BEGINNER, INTERMEDIATE, ADVANCED)
            count: Number of words to generate
            
        Returns:
            List of dictionaries containing word, persian meaning, and synonyms
        """
        prompt = f"""Generate {count} {level.lower()} level English words with their Persian translations and synonyms.
        The words should be appropriate for English language learners at {level.lower()} level.
        Format the response as a JSON array with the following structure for each word:
        [
            {{"word": "example", "persian": "مثال", "synonyms": ["instance", "sample"]}},
            ...
        ]
        Ensure each Persian translation is accurate and the synonyms are at a similar difficulty level."""

        try:
            response = self.model.generate_content(prompt)
            # Extract the JSON string from the response
            json_str = response.text.strip()
            # If the response is wrapped in code blocks, remove them
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"Error generating words with Gemini: {str(e)}")
            # Return a default word list in case of error
            return [
                {"word": "error", "persian": "خطا", "synonyms": ["mistake", "fault"]},
            ] * count
