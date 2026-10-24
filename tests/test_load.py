from sqlalchemy import text
from src.load import ensure_table_exists, load_articles
from src.transform import transform_articles


def test_ensure_table_exists(memory_db_engine):
    table = ensure_table_exists(memory_db_engine, table_name="test_news")
    assert table.name == "test_news"

    with memory_db_engine.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='test_news'")
        ).fetchone()
        assert row is not None


def test_load_articles_append_and_replace(memory_db_engine, sample_raw_articles):
    df = transform_articles(sample_raw_articles)

    written = load_articles(df, engine=memory_db_engine, table_name="test_articles", if_exists="append")
    assert written == 2

    with memory_db_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM test_articles")).scalar()
        assert count == 2

    load_articles(df, engine=memory_db_engine, table_name="test_articles", if_exists="append")
    with memory_db_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM test_articles")).scalar()
        assert count == 4

    load_articles(df, engine=memory_db_engine, table_name="test_articles", if_exists="replace")
    with memory_db_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM test_articles")).scalar()
        assert count == 2


def test_load_articles_empty_dataframe(memory_db_engine):
    import pandas as pd
    written = load_articles(pd.DataFrame(), engine=memory_db_engine, table_name="test_empty")
    assert written == 0
