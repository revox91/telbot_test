from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_URL: str
    REDIS_DB: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


CONFIG = Settings()
