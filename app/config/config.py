from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv()


class Settings(BaseSettings):
    db_echo: bool = False
    # db_echo: bool = True
    SETTINGS_DB_HOST: str
    SETTINGS_DB_PORT: int
    SETTINGS_DB_NAME: str
    SETTINGS_DB_USER: str
    SETTINGS_DB_PASSWORD: str

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.SETTINGS_DB_USER}:{self.SETTINGS_DB_PASSWORD}@{self.SETTINGS_DB_HOST}:{self.SETTINGS_DB_PORT}/{self.SETTINGS_DB_NAME}"


settings = Settings()
