import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from sportradar_api import SoccerExtendedPandas
from utils.utils import upsert_data_to_db

from airflow import DAG


def get_competitions():
    sportradar = SoccerExtendedPandas()
    competitions = sportradar.get_competitions()
    upsert_data_to_db(competitions, table="competitions", primary_keys=["id"])


def get_seasons():
    sportradar = SoccerExtendedPandas()
    seasons = sportradar.get_seasons()
    upsert_data_to_db(seasons, table="seasons", primary_keys=["id"])


with DAG(
    dag_id="football_players_etl",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:
    get_competitions = PythonOperator(
        task_id="get_competitions",
        python_callable=get_competitions,
    )

    get_seasons = PythonOperator(
        task_id="get_seasons",
        python_callable=get_seasons,
    )

get_competitions >> get_seasons
