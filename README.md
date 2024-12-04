# English Learning Stories API

This FastAPI application helps users practice English by providing level-appropriate stories based on their chosen topics and proficiency levels.

## Features

- Generate or retrieve stories based on topic and English proficiency level
- Stories are tailored to match the user's English level (beginner, intermediate, advanced)
- Uses Groq AI with Mixtral-8x7b model for high-quality story generation
- Persistent storage of stories in SQLite database
- RESTful API endpoints for story retrieval and generation

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /stories/
Generate or retrieve a story based on topic and English level.

Request body:
```json
{
    "topic": "string",
    "level": "beginner|intermediate|advanced"
}
```

### GET /stories/
List all stories, optionally filtered by topic and/or level.

Query parameters:
- `topic` (optional): Filter stories by topic
- `level` (optional): Filter stories by English level

## Database

The application uses SQLite as its database. The database file `stories.db` will be created automatically in the root directory when you first run the application.
