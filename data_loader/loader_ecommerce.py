import os
import logging
from pyspark.sql import SparkSession, DataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_ecommerce(spark: SparkSession) -> DataFrame:
    """
    Carica il dataset ecommerce.csv e restituisce un DataFrame Spark.
    """
    path = os.path.join("data", "ecommerce.csv")

    if not os.path.exists(path):
        logger.error(f"[Ecommerce Loader] File non trovato: {path}")
        raise FileNotFoundError(f"File non trovato: {path}")

    logger.info(f"[Ecommerce Loader] Caricamento da: {path}")

    df = spark.read.csv(path, header=True, inferSchema=True)

    logger.debug(f"[Ecommerce Loader] Righe caricate: {df.count()}")
    return df
