from pyspark.sql.functions import year

def show_sales_by_store(dfs, filters):
    """
    Mostra il totale delle vendite per negozio in un dato anno.
    """
    train_df = dfs["train"]

    if "year" in filters:
        train_df = train_df.withColumn("year", year("Date"))
        train_df = train_df.filter(train_df["year"] == filters["year"])

    return train_df.groupBy("Store").sum("Sales").orderBy("sum(Sales)", ascending=False)