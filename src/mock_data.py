from typing import Any, Dict, List

SAMPLE_ARTICLES: List[Dict[str, Any]] = [
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
    {
        "source": {"id": "reuters", "name": "Reuters"},
        "author": "Stephen Nellis",
        "title": "Global semiconductor market hits record capital expenditure high",
        "description": "Semiconductor manufacturers worldwide increased quarterly investments in advanced lithography and packaging infrastructure.",
        "url": "https://reuters.com/technology/semiconductor-capex-record-high-2026-05-11",
        "urlToImage": "https://reuters.com/wp-content/uploads/chips.jpg",
        "publishedAt": "2026-05-11T12:00:00Z",
        "content": "Spending on semiconductor manufacturing equipment jumped by 18 percent year over year driven by surging demand for AI server clusters.",
    },
    {
        "source": {"id": "wired", "name": "Wired"},
        "author": "Steven Levy",
        "title": "Open source data engineering frameworks embrace distributed stream processors",
        "description": "The data infrastructure landscape continues to evolve as unified storage and streaming engines gain mainstream adoption.",
        "url": "https://wired.com/story/data-engineering-stream-processors-2026",
        "urlToImage": "https://wired.com/wp-content/uploads/data.jpg",
        "publishedAt": "2026-05-11T17:45:00Z",
        "content": "Modern distributed computing has fundamentally transformed how cloud enterprises ingest, validate, and query real-time data streams.",
    },
    {
        "source": {"id": "bloomberg", "name": "Bloomberg"},
        "author": "Mark Gurman",
        "title": "Cloud providers expand renewable energy procurement for gigawatt data centers",
        "description": "Major hyperscalers have secured multi-gigawatt nuclear and geothermal power purchase agreements across North America.",
        "url": "https://bloomberg.com/news/articles/2026-05-11/cloud-providers-clean-power",
        "urlToImage": "https://bloomberg.com/wp-content/uploads/power.jpg",
        "publishedAt": "2026-05-11T18:30:00Z",
        "content": "Surging electrical demands from high-density compute facilities have accelerated long-term contracts with clean energy suppliers.",
    },
]


def get_mock_articles(query: str = "technology") -> Dict[str, Any]:
    filtered = [
        a for a in SAMPLE_ARTICLES
        if query.lower() in a["title"].lower() or query.lower() in a["description"].lower()
    ]
    selected = filtered if filtered else SAMPLE_ARTICLES
    return {
        "status": "ok",
        "totalResults": len(selected),
        "articles": selected,
    }
