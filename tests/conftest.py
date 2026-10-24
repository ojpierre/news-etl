from typing import Any, Dict, List
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@pytest.fixture
def sample_raw_articles() -> List[Dict[str, Any]]:
    return [
        {
            "source": {"id": "techcrunch", "name": "TechCrunch"},
            "author": "Sarah Perez",
            "title": "OpenAI announces new enterprise compliance and security controls",
            "description": "OpenAI has expanded its enterprise developer platform with granular audit logs and custom access policies.",
            "url": "https://techcrunch.com/2026/05/11/openai-enterprise-controls",
            "urlToImage": "https://techcrunch.com/wp-content/uploads/openai.jpg",
            "publishedAt": "2026-05-11T14:30:00Z",
            "content": "OpenAI today announced a collection of security and data governance features designed specifically for Fortune 500 engineering organizations.",
        },
        {
            "source": {"id": "the-verge", "name": "The Verge"},
            "author": "Dieter Bohn",
            "title": "Apple unveils M5 architecture with unified hardware accelerators",
            "description": "The latest Apple silicon chips introduce dedicated tensor engines for edge device inference and efficiency.",
            "url": "https://theverge.com/2026/05/11/apple-m5-announcement",
            "urlToImage": "https://theverge.com/wp-content/uploads/m5.jpg",
            "publishedAt": "2026-05-11T16:15:00Z",
            "content": "Apple has officially taken the wraps off its next generation M5 processor family promising 40 percent faster multi-core performance.",
        },
    ]


@pytest.fixture
def memory_db_engine() -> Engine:
    return create_engine("sqlite:///:memory:")
