import os
import logging
from pyspark.sql import SparkSession, DataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_hr(spark: SparkSession) -> DataFrame:
    """
    Carica il dataset HR da data/hr.csv
    """
    path = os.path.join("data", "hr.csv")

    if not os.path.exists(path):
        logger.error(f"[HR Loader] File non trovato: {path}")
        raise FileNotFoundError(f"File non trovato: {path}")

    logger.info(f"[HR Loader] Caricamento da: {path}")

    df = spark.read.csv(path, header=True, inferSchema=True)

    logger.debug(f"[HR Loader] Righe caricate: {df.count()}")
    return df
