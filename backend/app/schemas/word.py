from pydantic import BaseModel
from typing import List, Optional

class WordRequest(BaseModel):
    word: str
    persian_meaning: str
    synonyms: Optional[List[str]] = None

class WordResponse(WordRequest):
    id: Optional[int] = None
