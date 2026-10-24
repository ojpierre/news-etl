from datetime import datetime, timedelta
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    AIRFLOW_AVAILABLE = True
except ImportError:
    try:
        from airflow.providers.standard.operators.python import PythonOperator
        from airflow import DAG
        AIRFLOW_AVAILABLE = True
    except ImportError:
        AIRFLOW_AVAILABLE = False

from src.extract import extract_articles
from src.transform import transform_articles
from src.load import load_articles


def run_extract_task(**context):
    articles = extract_articles()
    return articles


def run_transform_task(**context):
    ti = context["ti"]
    articles = ti.xcom_pull(task_ids="extract_news_data")
    df = transform_articles(articles or [])
    return df.to_dict(orient="records")


def run_load_task(**context):
    ti = context["ti"]
    records = ti.xcom_pull(task_ids="transform_news_data")
    import pandas as pd
    df = pd.DataFrame(records or [])
    return load_articles(df)


default_args = {
    "owner": "Peter",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

if AIRFLOW_AVAILABLE:
    dag = DAG(
        "news_article_pipeline",
        default_args=default_args,
        description="Extract, transform, and load news articles into analytical database",
        schedule="@daily",
        catchup=False,
    )

    extract_task = PythonOperator(
        task_id="extract_news_data",
        python_callable=run_extract_task,
        dag=dag,
    )

    transform_task = PythonOperator(
        task_id="transform_news_data",
        python_callable=run_transform_task,
        dag=dag,
    )

    load_task = PythonOperator(
        task_id="load_news_data",
        python_callable=run_load_task,
        dag=dag,
    )

    extract_task >> transform_task >> load_task
