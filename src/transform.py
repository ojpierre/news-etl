import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Union
import pandas as pd

logger = logging.getLogger(__name__)


def _classify_topic(text: str) -> str:
    lower_text = text.lower()
    if re.search(r"\b(ai|artificial intelligence|machine learning|llm|neural|openai|deepmind|anthropic)\b", lower_text):
        return "AI & Machine Learning"
    if re.search(r"\b(chip|semiconductor|hardware|processor|lithography|gpu|nvidia|intel|arm)\b", lower_text):
        return "Hardware & Silicon"
    if re.search(r"\b(cloud|kubernetes|docker|infrastructure|server|datacenter|aws|azure)\b", lower_text):
        return "Cloud & Infrastructure"
    if re.search(r"\b(market|shares|stock|capital|revenue|nasdaq|quarterly|invest|capex)\b", lower_text):
        return "Markets & Finance"
    if re.search(r"\b(cybersecurity|security|malware|vulnerability|hacker|breach|encryption)\b", lower_text):
        return "Security & Privacy"
    return "General Tech"


def _estimate_word_count(content: str, description: str) -> int:
    text_pool = f"{content or ''} {description or ''}".strip()
    if not text_pool:
        return 0
    clean_text = re.sub(r"\[\+\d+ chars\]", "", text_pool)
    tokens = [tok for tok in clean_text.split() if tok.strip()]
    return len(tokens)


def transform_articles(articles: Union[List[Dict[str, Any]], Dict[str, Any], pd.DataFrame]) -> pd.DataFrame:
    if isinstance(articles, pd.DataFrame):
        raw_items = articles.to_dict(orient="records")
    elif isinstance(articles, dict):
        raw_items = articles.get("articles", [articles])
    elif isinstance(articles, list):
        raw_items = articles
    else:
        raise ValueError(f"Unsupported articles payload type: {type(articles)}")

    if not raw_items:
        logger.warning("Empty articles payload provided; returning empty DataFrame.")
        return pd.DataFrame(
            columns=[
                "source_name",
                "author",
                "title",
                "description",
                "url",
                "published_at",
                "content",
                "word_count",
                "reading_time_minutes",
                "topic_category",
                "ingested_at",
            ]
        )

    records: List[Dict[str, Any]] = []
    for item in raw_items:
        source = item.get("source") or {}
        source_name = source.get("name") if isinstance(source, dict) else item.get("source_name")

        record = {
            "source_name": source_name or "Unknown",
            "author": item.get("author") or "Staff",
            "title": item.get("title") or "",
            "description": item.get("description") or "",
            "url": item.get("url") or "",
            "published_at": item.get("publishedAt") or item.get("published_at"),
            "content": item.get("content") or "",
        }
        records.append(record)

    df = pd.DataFrame(records)

    df = df[df["title"].str.strip() != "[Removed]"]
    df = df[df["title"].str.strip() != ""]
    df = df[df["url"].str.strip() != ""]

    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")

    df["word_count"] = df.apply(
        lambda r: _estimate_word_count(r["content"], r["description"]),
        axis=1,
    )
    df["reading_time_minutes"] = df["word_count"].apply(lambda count: max(1, round(count / 200)))

    df["topic_category"] = df.apply(
        lambda r: _classify_topic(f"{r['title']} {r['description']}"),
        axis=1,
    )

    df["ingested_at"] = datetime.now(timezone.utc)

    df.drop_duplicates(subset=["url"], keep="last", inplace=True)
    df.reset_index(drop=True, inplace=True)

    ordered_cols = [
        "source_name",
        "author",
        "title",
        "description",
        "url",
        "published_at",
        "content",
        "word_count",
        "reading_time_minutes",
        "topic_category",
        "ingested_at",
    ]
    df = df[[col for col in ordered_cols if col in df.columns]]

    logger.info("Transformed %d news articles successfully.", len(df))
    return df
