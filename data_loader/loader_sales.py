import os
import logging
from pyspark.sql import SparkSession, DataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Mappa nomi logici → file nel folder /data
_FILES = {
    "train": "train.csv",
    "store": "store.csv",
    "test": "test.csv",
    "sample_submission": "sample_submission.csv",
}

def load_sales(spark: SparkSession) -> dict[str, DataFrame]:
    """
    Carica i dataset relativi alle vendite:
    - train.csv
    - store.csv
    - test.csv
    - sample_submission.csv

    Restituisce un dizionario di DataFrame:
    {
        "train": ...,
        "store": ...,
        "test": ...,
        "sample_submission": ...
    }
    """
    base_path = "data"
    dataframes = {}

    for name, filename in _FILES.items():
        path = os.path.join(base_path, filename)

        if not os.path.exists(path):
            logger.warning(f"[Sales Loader] File mancante: {path}")
            continue

        logger.info(f"[Sales Loader] Caricamento {name} da: {path}")
        df = spark.read.csv(path, header=True, inferSchema=True)
        dataframes[name] = df

    if not dataframes:
        raise RuntimeError("Nessun file vendite trovato nella cartella 'data/'.")

    return dataframes
