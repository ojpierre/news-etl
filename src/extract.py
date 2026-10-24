import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import requests

try:
    from .config import settings
    from .mock_data import get_mock_articles
except ImportError:
    from config import settings
    from mock_data import get_mock_articles

logger = logging.getLogger(__name__)


def extract_articles(
    query: str = "technology",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_by: str = "popularity",
    language: str = "en",
    page_size: int = 50,
    api_key: Optional[str] = None,
    use_mock: bool = False,
    timeout: int = 15,
) -> List[Dict[str, Any]]:
    resolved_key = api_key or settings.api_key
    search_query = query.strip() or settings.default_query

    if use_mock or not resolved_key:
        if not resolved_key:
            logger.warning(
                "No NewsAPI key found in environment; falling back to offline mock dataset for query '%s'.",
                search_query,
            )
        data = get_mock_articles(query=search_query)
        return data.get("articles", [])

    if not from_date:
        from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

    endpoint = f"{settings.base_url}/everything"
    params: Dict[str, Any] = {
        "q": search_query,
        "from": from_date,
        "sortBy": sort_by,
        "language": language or settings.default_language,
        "pageSize": min(page_size, 100),
        "apiKey": resolved_key,
    }
    if to_date:
        params["to"] = to_date

    logger.info(
        "Fetching news articles from NewsAPI for query='%s' (from=%s, sortBy=%s)...",
        search_query,
        from_date,
        sort_by,
    )

    try:
        response = requests.get(endpoint, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            message = data.get("message", "NewsAPI returned an unsuccessful status")
            raise RuntimeError(f"NewsAPI error: {message}")

        articles = data.get("articles", [])
        logger.info("Successfully extracted %d raw articles from NewsAPI.", len(articles))
        return articles
    except requests.RequestException as exc:
        logger.error("HTTP request failed while fetching news: %s", exc)
        raise
