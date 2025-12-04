# Lamoda.kz — Mini Data Pipeline


## Target
Category: Men → Running
URL: https://www.lamoda.kz/c/3949/default-sport_men_run/


## Collected fields
- name
- brand
- price


## How to run
1. Install Python 3.10+.
2. Create venv.
3. `pip install -r requirements.txt`
4. `playwright install`


### Local run
1. `python src/scraper.py` # -> data/raw_products.json
2. `python src/cleaner.py` # -> data/clean_products.csv
3. `python src/loader.py` # -> data/output.db


### Airflow
1. Set `AIRFLOW_HOME` и `airflow db init`
2. Put `airflow_dag.py` into `${AIRFLOW_HOME}/dags/`
3. `airflow users create ...`
4. `airflow webserver -p 8080` и `airflow scheduler`
5. В UI запустить DAG `lamoda_pipeline` вручную для первого прогона.