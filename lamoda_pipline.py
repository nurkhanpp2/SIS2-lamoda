from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from scraper import run as run_scraper
from cleaner import run as run_cleaner
from loader import run as run_loader


default_args = {
    'owner': 'team',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}


with DAG(
    dag_id='lamoda_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 12, 1),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:


    t1 = PythonOperator(
        task_id='scrape',
        python_callable=run_scraper,
    )


    t2 = PythonOperator(
        task_id='clean',
        python_callable=run_cleaner,
    )


    t3 = PythonOperator(
        task_id='load',
        python_callable=run_loader,
    )

    t1 >> t2 >> t3
