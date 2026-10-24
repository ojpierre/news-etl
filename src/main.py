import argparse
import logging
import sys
from typing import List, Optional

try:
    from .config import settings
    from .extract import extract_articles
    from .load import load_articles
    from .transform import transform_articles
except ImportError:
    from config import settings
    from extract import extract_articles
    from load import load_articles
    from transform import transform_articles

logger = logging.getLogger("news_etl")


def setup_logging(log_level: str = "INFO") -> None:
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def run_pipeline(
    query: str = "technology",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_by: str = "popularity",
    database_url: Optional[str] = None,
    mode: str = "append",
    use_mock: bool = False,
) -> int:
    logger.info("Starting News Articles ETL Pipeline")
    logger.info("Query: '%s' | Sort: %s | Mode: %s | Mock: %s", query, sort_by, mode, use_mock)

    raw_articles = extract_articles(
        query=query,
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by,
        use_mock=use_mock,
    )
    if not raw_articles:
        logger.warning("No articles extracted. Exiting pipeline.")
        return 0

    articles_df = transform_articles(raw_articles)
    if articles_df.empty:
        logger.warning("No valid articles produced after transformation.")
        return 0

    rows_loaded = load_articles(
        articles_df=articles_df,
        engine=database_url,
        if_exists=mode,
    )

    logger.info("Pipeline Execution Summary:")
    logger.info(" - Total articles loaded: %d", rows_loaded)
    if "topic_category" in articles_df.columns:
        topic_counts = articles_df["topic_category"].value_counts().to_dict()
        logger.info(" - Category breakdown: %s", topic_counts)
    if "source_name" in articles_df.columns:
        top_sources = articles_df["source_name"].value_counts().head(3).to_dict()
        logger.info(" - Top publishers: %s", top_sources)
    if "reading_time_minutes" in articles_df.columns:
        avg_read_time = articles_df["reading_time_minutes"].mean()
        logger.info(" - Average reading time: %.1f min", avg_read_time)

    logger.info("ETL process completed successfully!")
    return rows_loaded


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="News ETL Pipeline - Ingest, normalize, categorize, and store articles from NewsAPI."
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        default=settings.default_query,
        help="Search keyword or topic query (e.g. Apple, Artificial Intelligence, Semiconductor).",
    )
    parser.add_argument(
        "--from-date",
        type=str,
        default=None,
        help="Start date filter in YYYY-MM-DD format (defaults to 7 days ago).",
    )
    parser.add_argument(
        "--to-date",
        type=str,
        default=None,
        help="End date filter in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["popularity", "publishedAt", "relevancy"],
        default="popularity",
        help="Article sort order (default: popularity).",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=None,
        help="Database connection URL override (SQLite or PostgreSQL).",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["append", "replace"],
        default="append",
        help="Database table load mode: append or replace (default: append).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run pipeline using built-in synthetic news dataset without API calls.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging verbosity level (default: INFO).",
    )
    return parser


def main(args: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    setup_logging(parsed_args.log_level)

    try:
        run_pipeline(
            query=parsed_args.query,
            from_date=parsed_args.from_date,
            to_date=parsed_args.to_date,
            sort_by=parsed_args.sort_by,
            database_url=parsed_args.db_url,
            mode=parsed_args.mode,
            use_mock=parsed_args.mock,
        )
        return 0
    except Exception as exc:
        logger.exception("Pipeline terminated with unhandled exception: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
