# executor.py

from pyspark.sql import SparkSession
from config.settings import SPARK_LOG_LEVEL
from data_loader.loader_registry import get_loader

def create_spark_session():
    return (
        SparkSession.builder
        .appName("DataWhiz Enterprise")
        .getOrCreate()
    )

def preload_dataframes(spark):
    """
    Carica in anticipo i DataFrame più comuni in un dizionario.
    """
    df_map = {
        "hr_df": get_loader("hr")(spark),
        "sales_df": get_loader("sales")(spark),
        "ecommerce_df": get_loader("ecommerce")(spark),
    }
    return df_map

def execute_code(code: str):
    """
    Esegue codice Python dinamico contenente operazioni Spark.
    Il codice deve assegnare il risultato finale alla variabile `result`.
    """
    spark = create_spark_session()
    spark.sparkContext.setLogLevel(SPARK_LOG_LEVEL)

    local_vars = {"spark": spark}
    local_vars.update(preload_dataframes(spark))  # <--- Qui carichiamo hr_df, etc.

    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        return result
    except Exception as e:
        print(f"[Executor] Errore nell'esecuzione del codice: {e.__class__.__name__} – {e}")
        print("[Executor] Codice fallito:")
        print(code)
        return None
