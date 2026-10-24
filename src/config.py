import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("NEWS_API_KEY") or os.getenv("NEWSAPI_KEY", "")
    base_url: str = "https://newsapi.org/v2"
    default_query: str = os.getenv("DEFAULT_QUERY", "technology")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")
    database_url: str = ""

    def get_database_url(self) -> str:
        if self.database_url:
            return self._normalize_db_url(self.database_url)

        env_db_url = os.getenv("DATABASE_URL")
        if env_db_url:
            return self._normalize_db_url(env_db_url)

        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")

        if db_user and db_name:
            return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return "sqlite:///news_articles.db"

    @staticmethod
    def _normalize_db_url(url: str) -> str:
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url


settings = Settings()
