from bs4 import BeautifulSoup
from clickhouse_driver import Client
import pandas as pd
import re
from tqdm import tqdm

import constants


def get_ch_client():
    with open(constants.CLICKHOUSE_CONFIG_FILEPATH, "r") as f:
        ch_config = f.read()
    ch_config = BeautifulSoup(ch_config, "xml")
    ch_client = Client(
        host=ch_config.find("host").text,
        port=ch_config.find("port").text,
        user=ch_config.find("user").text,
        password=ch_config.find("password").text,
        secure=ch_config.find("secure").text,
    )
    return ch_client


def get_table_colnames(client, db, table):
    return [i[0] for i in client.execute(f"describe {db}.{table}")]


def query_dataframe_pb(client, query):
    """
    Prints progress bar on query execution and parses query output to pd.DataFrame.
    """
    progress = client.execute_with_progress(query, columnar=True, with_column_types=True)
    for num_rows, total_rows in progress:
        if total_rows:
            done = float(num_rows) / total_rows
        else:
            done = total_rows
        if "pbar" not in locals():
            pbar = tqdm(total=total_rows, desc="Querying data from ClickHouse")
        pbar.update(num_rows - pbar.n)
    pbar.close()
    data, columns = progress.get_result()
    return pd.DataFrame(
        {re.sub(r'\W', '_', col[0]): d for d, col in zip(data, columns)}
    )
