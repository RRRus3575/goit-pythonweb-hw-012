import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import redis

load_dotenv(dotenv_path=os.getenv("ENV_FILE_PATH", "/etc/secrets/.env"))

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


print("🔍 DATABASE_URL:", os.getenv("DATABASE_URL"))
print("🔍 JWT_SECRET_KEY:", os.getenv("JWT_SECRET_KEY"))
print("🔍 REDIS_URL:", os.getenv("REDIS_URL"))
print("🔍 SMTP_USER:", os.getenv("SMTP_USER"))


settings = Settings()

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
