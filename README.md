# News ETL

A Python ETL pipeline that fetches popular Apple-related articles from NewsAPI, cleans the data with pandas, and loads the results into PostgreSQL.

## Pipeline

1. **Extract**: Requests articles from the NewsAPI `everything` endpoint.
2. **Transform**: Converts the response into a DataFrame and removes unnecessary columns.
3. **Load**: Replaces the PostgreSQL `articles_main` table with the transformed data.

The pipeline can run locally through `src/main.py` or on a daily schedule through the `news_article_pipeline` Airflow DAG.

## Requirements

- Python 3.10+
- PostgreSQL
- A NewsAPI key
- Apache Airflow for scheduled execution

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root. It should contain:

```env
NEWS_API_KEY=your_news_api_key
DB_HOST=localhost
DB_USER=your_database_user
DB_NAME=your_database_name
DB_PASSWORD=your_database_password
DB_PORT=5432
```

Do not commit `.env`; it is excluded by `.gitignore`.

## Run Locally

```bash
python src/main.py
```

## Airflow

The DAG is located at `dags/news.dag.py` and runs daily with one retry after five minutes. To use it, configure Airflow to scan this project's `dags` directory, then enable the `news_article_pipeline` DAG in Airflow.

## Project Structure

```text
news_etl/
├── dags/
│   └── news.dag.py
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

