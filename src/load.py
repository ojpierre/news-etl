import logging
from typing import Optional, Union
import pandas as pd
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)
from sqlalchemy.engine import Engine

try:
    from .config import settings
except ImportError:
    from config import settings

logger = logging.getLogger(__name__)

TABLE_NAME = "news_articles"


def get_engine(database_url: Optional[str] = None) -> Engine:
    url = database_url or settings.get_database_url()
    return create_engine(url, pool_pre_ping=True)


def ensure_table_exists(engine: Engine, table_name: str = TABLE_NAME) -> Table:
    metadata = MetaData()
    table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("source_name", String(150), index=True, nullable=False),
        Column("author", String(255), nullable=True),
        Column("title", String(500), index=True, nullable=False),
        Column("description", Text, nullable=True),
        Column("url", String(1000), index=True, nullable=False),
        Column("published_at", DateTime(timezone=True), index=True, nullable=True),
        Column("content", Text, nullable=True),
        Column("word_count", Integer, nullable=True),
        Column("reading_time_minutes", Integer, nullable=True),
        Column("topic_category", String(100), index=True, nullable=True),
        Column("ingested_at", DateTime(timezone=True), nullable=False),
    )
    metadata.create_all(engine)
    return table


def load_articles(
    articles_df: pd.DataFrame,
    engine: Optional[Union[Engine, str]] = None,
    table_name: str = TABLE_NAME,
    if_exists: str = "append",
) -> int:
    if articles_df.empty:
        logger.warning("Empty DataFrame provided to load stage; skipping database write.")
        return 0

    if engine is None:
        db_engine = get_engine()
    elif isinstance(engine, str):
        db_engine = get_engine(engine)
    else:
        db_engine = engine

    ensure_table_exists(db_engine, table_name=table_name)

    logger.info(
        "Loading %d articles into database table '%s' (mode: %s)...",
        len(articles_df),
        table_name,
        if_exists,
    )

    with db_engine.begin() as connection:
        articles_df.to_sql(
            name=table_name,
            con=connection,
            if_exists=if_exists,
            index=False,
            method="multi",
        )

    logger.info("Successfully loaded %d articles into '%s'.", len(articles_df), table_name)
    return len(articles_df)
