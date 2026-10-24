import pytest
from src.extract import extract_articles


def test_extract_articles_mock():
    articles = extract_articles(query="technology", use_mock=True)
    assert isinstance(articles, list)
    assert len(articles) > 0
    assert "title" in articles[0]
    assert "url" in articles[0]


def test_extract_articles_fallback_no_api_key(monkeypatch):
    monkeypatch.delenv("NEWS_API_KEY", raising=False)
    monkeypatch.delenv("NEWSAPI_KEY", raising=False)

    articles = extract_articles(query="technology", api_key="", use_mock=False)
    assert isinstance(articles, list)
    assert len(articles) > 0


def test_extract_articles_api_failure(mocker):
    mock_get = mocker.patch("requests.get")
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"status": "error", "message": "apiKeyMissing"}
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="apiKeyMissing"):
        extract_articles(query="apple", api_key="test_dummy_key", use_mock=False)
