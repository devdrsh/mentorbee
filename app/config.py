import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    
    _raw_db_url = os.getenv("DATABASE_URL", "sqlite:///./mentorbee.db")
    # Render and Heroku provide postgres:// which SQLAlchemy 1.4+ rejects; normalize to postgresql://
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = _raw_db_url

settings = Settings()

