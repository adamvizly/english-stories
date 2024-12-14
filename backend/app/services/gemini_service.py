import os
import json
import google.generativeai as genai
from typing import List, Dict, Optional, Tuple, Any
from fastapi import HTTPException

class GeminiService:
    def __init__(self):
        # Set up the Gemini API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_story(self, topic: str, level: str) -> str:
        """
        Generate a story based on topic and level.
        
        Args:
            topic (str): Story topic
            level (str): English level
        
        Returns:
            str: Generated story content
        """
        # Craft prompt based on level
        level_descriptions = {
            "BEGINNER": "simple vocabulary and basic sentence structures",
            "INTERMEDIATE": "moderate vocabulary and compound sentences",
            "ADVANCED": "rich vocabulary, complex sentences, and idiomatic expressions"
        }

        prompt = f"""Generate a short story about {topic}. 
        The story should be suitable for {level.lower()} English learners, 
        using {level_descriptions.get(level, 'simple language')}.
        The story should be engaging and include a clear beginning, middle, and end.
        Focus on creating an interesting narrative that helps language learners.
        
        Provide only the story text, without any additional commentary."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating story: {e}")
            return f"A story about {topic} could not be generated."

    def extract_grammar_notes(self, story_content: str) -> List[Dict]:
        """
        Extract grammar notes from a story.
        
        Args:
            story_content (str): Story text to analyze
        
        Returns:
            List of grammar note dictionaries
        """
        prompt = f"""Analyze the following story and identify 3 key grammar concepts used:

        Story: {story_content}

        For each grammar concept, provide:
        1. The name of the grammar concept
        2. A clear, concise explanation
        3. 2-3 example sentences from the story

        Return the response as a valid JSON array of objects with these keys:
        - 'concept': string
        - 'explanation': string
        - 'examples': list of strings

        Example output:
        [
            {{
                "concept": "Past Simple Tense",
                "explanation": "Used to describe completed actions in the past",
                "examples": [
                    "She walked to the store",
                    "He bought a new book"
                ]
            }},
            ...
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from the response
            json_match = response.text.strip()
            
            # Try to parse the response as JSON
            try:
                grammar_notes = json.loads(json_match)
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from markdown code block
                start = json_match.find('```json')
                end = json_match.find('```', start + 7)
                if start != -1 and end != -1:
                    json_match = json_match[start+7:end].strip()
                    grammar_notes = json.loads(json_match)
                else:
                    # Fallback: try to parse without code block markers
                    grammar_notes = json.loads(json_match)
            
            return grammar_notes
        
        except Exception as e:
            print(f"Error extracting grammar notes: {e}")
            return []

    def generate_words(self, level: str) -> List[Dict]:
        """
        Generate daily words based on the user's English level.
        
        Args:
            level (str): User's English level (BEGINNER, INTERMEDIATE, ADVANCED)
        
        Returns:
            List of dictionaries containing word details
        """
        # Prompt to generate words with specific details
        prompt = f"""
        Generate 5 unique English words suitable for a {level.lower()} level English learner. 
        For each word, provide:
        1. The word itself
        2. Its Persian meaning
        3. 2-3 synonyms
        
        Return the response as a valid JSON array of objects with these keys:
        - 'word': string
        - 'persian_meaning': string
        - 'synonyms': list of strings
        
        Example output:
        [
            {{
                "word": "serendipity",
                "persian_meaning": "اتفاق خوشایند",
                "synonyms": ["chance", "luck"]
            }},
            ...
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from the response
            json_match = response.text.strip()
            
            # Try to parse the response as JSON
            try:
                words = json.loads(json_match)
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from markdown code block
                start = json_match.find('```json')
                end = json_match.find('```', start + 7)
                if start != -1 and end != -1:
                    json_match = json_match[start+7:end].strip()
                    words = json.loads(json_match)
                else:
                    # Fallback: try to parse without code block markers
                    words = json.loads(json_match)
            
            return words
        
        except Exception as e:
            print(f"Error generating words with Gemini: {e}")
            # Fallback words if generation fails
            return [
                {
                    "word": "resilience",
                    "persian_meaning": "مقاومت",
                    "synonyms": ["perseverance", "determination"]
                }
            ]

    def generate_story_with_grammar_notes(self, topic: str, level: str) -> Tuple[str, List[Dict]]:
        """
        Generate a story and its grammar notes in a single call.
        
        Args:
            topic (str): Story topic
            level (str): English level
        
        Returns:
            Tuple of (story_content, grammar_notes)
        """
        # Generate the story first
        story_content = self.generate_story(topic, level)
        
        # Extract grammar notes
        grammar_notes = self.extract_grammar_notes(story_content)
        
        return story_content, grammar_notes

    def extract_grammar_notes_from_content(self, story_content: str) -> List[Dict]:
        """
        Wrapper method to extract grammar notes from content.
        
        Args:
            story_content (str): Story text to analyze
        
        Returns:
            List of grammar note dictionaries
        """
        return self.extract_grammar_notes(story_content)

    def generate_word_with_details(self, level: str = 'BEGINNER') -> Dict[str, Any]:
        """
        Generate a word with its details using Gemini AI
        
        Args:
            level (str): Difficulty level of the word (BEGINNER, INTERMEDIATE, ADVANCED)
        
        Returns:
            Dict containing word details
        """
        prompt = f"""
        Generate a unique English word suitable for a {level} level learner. 
        Provide the following details in a JSON format:
        {{
            "word": "The English word",
            "persian_meaning": "Precise Persian translation",
            "synonyms": ["Synonym1", "Synonym2"],
            "example_sentence": "A clear example sentence using the word"
        }}

        Guidelines:
        - Choose words that are meaningful and useful
        - Provide accurate Persian translations
        - Include 2-3 synonyms
        - Create an example sentence that helps understand the word's usage
        """

        try:
            response = self.model.generate_content(prompt)
            # Parse the JSON response
            word_details = json.loads(response.text)
            
            return {
                'word': word_details['word'],
                'persian_meaning': word_details['persian_meaning'],
                'synonyms': word_details.get('synonyms', []),
                'example_sentence': word_details.get('example_sentence', '')
            }
        except Exception as e:
            # Raise an exception instead of returning a fallback word
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to generate word with AI: {str(e)}"
            )
