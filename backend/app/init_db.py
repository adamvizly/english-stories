from app.database import Base, engine
from app.models.auth import User
from app.models.story import Story

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database()
