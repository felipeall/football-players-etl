from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from sportradar_api import SoccerExtendedPandas
from utils.utils import fillna_numeric_cols, retrieve_missing_players, upsert_data_to_db

from airflow import DAG


def _parse_kwargs(kwargs: dict) -> list:
    params = kwargs.get("params")
    assert params, "Please trigger the DAG with a configuration JSON"

    seasons = params.get("seasons")

    assert seasons, 'Please use "seasons" as the JSON key. Example: {"seasons": ["sr:season:1", "sr:season:2", ...]}'
    assert isinstance(
        seasons, list
    ), 'Please use a list as the JSON value. Example: {"seasons": ["sr:season:1", "sr:season:2", ...]}'

    return seasons


def get_competitions():
    sportradar = SoccerExtendedPandas()
    competitions = sportradar.get_competitions()
    upsert_data_to_db(competitions, table="competitions", primary_keys=["id"])


def get_seasons():
    sportradar = SoccerExtendedPandas()
    seasons = sportradar.get_seasons()
    upsert_data_to_db(seasons, table="seasons", primary_keys=["id"])


def get_matches_statistics(**kwargs):
    seasons = _parse_kwargs(kwargs)
    sportradar = SoccerExtendedPandas()

    for season in seasons:
        matches_statistics = sportradar.get_season_matches_statistics(season_urn=season)
        matches_statistics = matches_statistics.dropna(subset=["players_id"])
        matches_statistics = fillna_numeric_cols(matches_statistics)
        upsert_data_to_db(matches_statistics, table="matches_statistics", primary_keys=["id", "players_id"])


def get_players(**kwargs):
    seasons = _parse_kwargs(kwargs)
    sportradar = SoccerExtendedPandas()

    for season in seasons:
        players = sportradar.get_season_competitor_player(season_urn=season)
        upsert_data_to_db(players, table="players", primary_keys=["id"])


def get_missing_players():
    players_missing = retrieve_missing_players()

    if players_missing:
        sportradar = SoccerExtendedPandas()

        for player_urn in players_missing:
            player = sportradar.get_player_profile_info(player_urn=player_urn)
            player = player.rename(columns={"player_id": "id"}).drop(columns="gender")
            upsert_data_to_db(player, table="players", primary_keys=["id"])


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

    get_matches_statistics = PythonOperator(
        task_id="get_matches_statistics",
        python_callable=get_matches_statistics,
    )

    get_players = PythonOperator(
        task_id="get_players",
        python_callable=get_players,
    )

    get_missing_players = PythonOperator(
        task_id="get_missing_players",
        python_callable=get_missing_players,
    )

get_competitions >> get_seasons >> get_matches_statistics >> get_players >> get_missing_players
