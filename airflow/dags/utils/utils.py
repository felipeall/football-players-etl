import random
import string

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy.engine import Engine


def create_engine() -> Engine:
    postgres_hook = PostgresHook("app_database_conn")
    engine = postgres_hook.get_sqlalchemy_engine()

    return engine


def generate_random_string(len_str: int = 15) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(len_str))


def upsert_data_to_db(df: pd.DataFrame, table: str, primary_keys: list) -> bool:
    temp_table = generate_random_string()
    cols = list(df.columns)
    cols_insert = ", ".join([f'"{col}"' for col in cols])
    cols_pk = ", ".join([f'"{col}"' for col in primary_keys])
    cols_update = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in cols if col not in primary_keys])
    query_temp_table = f"CREATE TEMPORARY TABLE {temp_table} AS SELECT * FROM {table} WHERE FALSE"
    query_upsert = f"""
            INSERT INTO {table} ({cols_insert})
            SELECT {cols_insert}
            FROM {temp_table}
            ON CONFLICT ({cols_pk})
            DO UPDATE SET
            {cols_update}, 
            updated_at = current_timestamp
        """

    with create_engine().begin() as con:
        con.exec_driver_sql(query_temp_table)
        df.to_sql(temp_table, con=con, index=False, if_exists="append")
        con.exec_driver_sql(query_upsert)

    return True


def retrieve_missing_players():
    query = """
        SELECT DISTINCT ms.players_id 
        FROM matches_statistics ms 
        LEFT JOIN players p
        ON p.id = ms.players_id 
        WHERE p.id IS NULL
        """

    engine = create_engine()

    with engine.begin() as con:
        res = con.exec_driver_sql(query)
        players_missing = res.scalars().all()

    return players_missing


def fillna_numeric_cols(df: pd.DataFrame, value: int = 0) -> pd.DataFrame:
    df = df.copy()
    for col in df:
        if df[col].dtype in ("int", "float"):
            df[col] = df[col].fillna(value)
    return df


def parse_kwargs(kwargs: dict) -> list:
    params = kwargs.get("params")
    assert params, "Please trigger the DAG with a configuration JSON"

    seasons = params.get("seasons")

    assert seasons, 'Please use "seasons" as the JSON key. Example: {"seasons": ["sr:season:1", "sr:season:2", ...]}'
    assert isinstance(
        seasons, list
    ), 'Please use a list as the JSON value. Example: {"seasons": ["sr:season:1", "sr:season:2", ...]}'

    return seasons
