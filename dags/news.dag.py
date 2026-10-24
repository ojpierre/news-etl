from datetime import datetime, timedelta
import os
import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.extract import extract_articles
from src.transform import transform_articles
from src.load import load_articles


default_args = {
    "owner": "Peter",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    "news_article_pipeline",
    default_args=default_args,
    description="Extract, transform, and load news articles",
    schedule="@daily",
    catchup=False,
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_news_data",
        python_callable=extract_articles,
    )
    
    transform_task = PythonOperator(
        task_id="transform_news_data",
        python_callable=transform_articles,
    )
    
    load_task = PythonOperator(
        task_id="load_news_data",
        python_callable=load_articles,
    )

    extract_task >> transform_task >> load_task
