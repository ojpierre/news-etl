import pandas as pd
from src.transform import transform_articles


def test_transform_unpacks_source_name(sample_raw_articles):
    df = transform_articles(sample_raw_articles)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "source_name" in df.columns
    assert df.iloc[0]["source_name"] == "TechCrunch"
    assert df.iloc[1]["source_name"] == "The Verge"


def test_transform_filters_removed_and_empty():
    bad_payload = [
        {"title": "[Removed]", "url": "https://example.com/removed", "source": {"name": "Example"}},
        {"title": "", "url": "https://example.com/empty", "source": {"name": "Example"}},
        {"title": "Valid Article", "url": "", "source": {"name": "Example"}},
        {"title": "Valid Article", "url": "https://example.com/valid", "source": {"name": "Example"}},
    ]
    df = transform_articles(bad_payload)
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Valid Article"


def test_transform_computes_word_count_and_read_time(sample_raw_articles):
    df = transform_articles(sample_raw_articles)
    assert "word_count" in df.columns
    assert "reading_time_minutes" in df.columns
    assert df.iloc[0]["word_count"] > 0
    assert df.iloc[0]["reading_time_minutes"] >= 1


def test_transform_classifies_topics(sample_raw_articles):
    df = transform_articles(sample_raw_articles)
    assert "topic_category" in df.columns
    assert df.iloc[0]["topic_category"] == "AI & Machine Learning"


def test_transform_drops_duplicates():
    duplicate_payload = [
        {"title": "First Version", "url": "https://example.com/dup", "source": {"name": "Test"}},
        {"title": "Updated Version", "url": "https://example.com/dup", "source": {"name": "Test"}},
    ]
    df = transform_articles(duplicate_payload)
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Updated Version"


def test_transform_empty_payload():
    df = transform_articles([])
    assert df.empty
    assert "source_name" in df.columns
