import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mentorbee.db")

settings = Settings()
