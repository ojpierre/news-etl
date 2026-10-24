# News Articles ETL Pipeline

[![CI Pipeline](https://github.com/ojpierre/news-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/ojpierre/news-etl/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-grade Python ETL pipeline that ingests current and historical news articles from NewsAPI, normalizes nested payload metadata, cleans invalid entries, computes content analytics (word count, reading time, topic categorization), and loads the curated records into a PostgreSQL or SQLite database using SQLAlchemy.

---

## Architecture Overview

`
                      +-----------------------------+
                      |      NewsAPI Service        |
                      |   (or Offline Mock Data)    |
                      +--------------+--------------+
                                     |
                                     | Extract (HTTP / requests)
                                     v
                      +-----------------------------+
                      |       src/extract.py        |
                      |  - Query & date range engine|
                      |  - Rate-limit/error handler |
                      +--------------+--------------+
                                     |
                                     | Raw Articles List
                                     v
                      +-----------------------------+
                      |      src/transform.py       |
                      |  - Unpack source name       |
                      |  - Filter [Removed] entries |
                      |  - Word count & read time   |
                      |  - Topic classification     |
                      |  - Deduplication & UTC ts   |
                      +--------------+--------------+
                                     |
                                     | Cleaned DataFrame
                                     v
                      +-----------------------------+
                      |        src/load.py          |
                      |  - SQLAlchemy 2.0 Engine    |
                      |  - Declarative Schema       |
                      |  - Append / Replace modes   |
                      +--------------+--------------+
                                     |
                       +-------------+-------------+
                       |                           |
                       v                           v
             +-------------------+       +-------------------+
             |    PostgreSQL     |       |   Local SQLite    |
             |   (Production)    |       |   (Development)   |
             +-------------------+       +-------------------+
`

---

## Features

- **Query Parameterization & Dynamic Date Filtering**: Extract articles by keyword (--query), date range (--from-date, --to-date), or sorting criteria (popularity, publishedAt, elevancy).
- **Data Enrichment & Content Analytics**:
  - source_name: Unpacks nested publisher metadata (e.g. *TechCrunch*, *The Verge*, *Reuters*).
  - word_count: Computes accurate article length metrics.
  - eading_time_minutes: Estimates reading duration based on standard reading speed benchmarks.
  - 	opic_category: Categorizes articles into tags (*AI & Machine Learning*, *Hardware & Silicon*, *Cloud & Infrastructure*, *Markets & Finance*, *Security & Privacy*, *General Tech*).
  - ingested_at: UTC timestamp recording pipeline execution time.
- **Data Quality & Sanitization**:
  - Automatically filters out takedown placeholders ([Removed]) and articles missing titles or target URLs.
  - Deduplicates records based on canonical article URLs.
- **Dual Database Engine Support**:
  - Supports **PostgreSQL** in production with connection pooling.
  - Automatically falls back to **SQLite** (sqlite:///news_articles.db) for immediate local development with zero external dependencies.
- **Offline / Sandbox Mode**: Includes a built-in mock dataset matching NewsAPI schema (--mock) allowing offline testing without paid API credentials.
- **Airflow Orchestration**: Includes a production-ready DAG in dags/news.dag.py with XCom task handoffs and retries.
- **Automated Testing & CI**: Comprehensive pytest test suite with automated GitHub Actions CI covering unit and end-to-end integration flows.

---

## Project Structure

`
news-etl/
+-- .github/
¦   +-- workflows/
¦       +-- ci.yml             # GitHub Actions CI workflow
+-- dags/
¦   +-- news.dag.py            # Airflow DAG for scheduled daily execution
+-- src/
¦   +-- __init__.py            # Package initializer
¦   +-- config.py              # Centralized environment and database configuration
¦   +-- extract.py             # Data extraction module (NewsAPI & mock client)
¦   +-- load.py                # Database loading module with SQLAlchemy schema
¦   +-- main.py                # Pipeline orchestrator and CLI entrypoint
¦   +-- mock_data.py           # Sample NewsAPI dataset for testing/demos
¦   +-- transform.py           # Data normalization, cleaning, and analytics
+-- tests/
¦   +-- __init__.py
¦   +-- conftest.py            # Test fixtures and in-memory SQLite database
¦   +-- test_extract.py        # Extraction and error handling tests
¦   +-- test_load.py           # Database schema and loading tests
¦   +-- test_pipeline.py       # End-to-end pipeline integration test
¦   +-- test_transform.py      # Transformation, typing, and analytics tests
+-- .env.example               # Example configuration file
+-- .gitignore                 # Git ignore rules
+-- LICENSE                    # MIT License
+-- pytest.ini                 # Pytest configuration
+-- README.md                  # Project documentation
+-- requirements.txt           # Python project dependencies
`

---

## Installation & Setup

1. **Clone the repository**:
   `ash
   git clone https://github.com/ojpierre/news-etl.git
   cd news-etl
   `

2. **Create and activate a virtual environment**:
   - **Linux / macOS**:
     `ash
     python -m venv venv
     source venv/bin/activate
     `
   - **Windows (PowerShell)**:
     `powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     `

3. **Install dependencies**:
   `ash
   pip install -r requirements.txt
   `

4. **Configure environment variables**:
   Create a .env file in the project root:
   `ash
   cp .env.example .env
   `

   Configure your credentials:
   `ini
   # NewsAPI credentials (https://newsapi.org)
   NEWS_API_KEY=your_news_api_key_here

   # Target database (defaults to SQLite if unset)
   DATABASE_URL=sqlite:///news_articles.db
   `

---

## Usage

### 1. Run with Mock Data (Zero Setup Demo)
To test the pipeline end-to-end without an external database or API key:
`ash
python src/main.py --mock --query "semiconductor"
`

### 2. Live API Extraction
Fetch recent technology news articles:
`ash
python src/main.py --query "artificial intelligence"
`

### 3. Date Range and Sort Order
Fetch articles within a custom window sorted by publication timestamp:
`ash
python src/main.py --query "Apple" --from-date 2026-05-01 --to-date 2026-05-15 --sort-by publishedAt
`

### 4. Database Load Modes
- ppend (default): Preserves historical ingestions and appends new records:
  `ash
  python src/main.py --mode append
  `
- eplace: Drops and recreates the target table before writing:
  `ash
  python src/main.py --mode replace
  `

---

## CLI Reference

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| --query | -q | Search keyword or topic | 	echnology |
| --from-date | | Start date filter (YYYY-MM-DD) | 7 days ago |
| --to-date | | End date filter (YYYY-MM-DD) | None |
| --sort-by | | Sort order (popularity, publishedAt, elevancy) | popularity |
| --db-url | | Database connection string override | Config / SQLite |
| --mode | | Table load mode: ppend or eplace | ppend |
| --mock | | Run using built-in synthetic dataset | False |
| --log-level | | Logging verbosity (DEBUG, INFO, WARNING, ERROR) | INFO |

---

## Database Schema (
ews_articles)

| Column Name | SQL Type | Description |
|-------------|----------|-------------|
| id | INTEGER | Primary Key, Auto-increment |
| source_name | VARCHAR(150) | Publishing outlet name (indexed) |
| uthor | VARCHAR(255) | Article author or staff byline |
| 	itle | VARCHAR(500) | Headline title (indexed) |
| description | TEXT | Article summary excerpt |
| url | VARCHAR(1000) | Canonical article link (indexed) |
| published_at | TIMESTAMP WITH TIME ZONE | Original publication timestamp (indexed) |
| content | TEXT | Article body content snippet |
| word_count | INTEGER | Estimated article token count |
| eading_time_minutes | INTEGER | Estimated reading duration in minutes |
| 	opic_category | VARCHAR(100) | Categorization tag (indexed) |
| ingested_at | TIMESTAMP WITH TIME ZONE | UTC ingestion timestamp |

---

## Airflow Orchestration

The Airflow DAG is located at dags/news.dag.py:
- **DAG ID**: 
ews_article_pipeline
- **Schedule**: @daily
- **Execution Flow**: extract_news_data >> transform_news_data >> load_news_data

To run in an Airflow environment:
1. Ensure your Airflow instance has access to this project root in PYTHONPATH.
2. Configure connections or environment variables (NEWS_API_KEY, DATABASE_URL).
3. Enable and trigger the DAG via the Airflow UI or CLI.

---

## Running Tests

Execute the complete test suite:
`ash
pytest -v
`

Run specific test modules:
`ash
pytest tests/test_extract.py -v
pytest tests/test_transform.py -v
pytest tests/test_load.py -v
pytest tests/test_pipeline.py -v
`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
