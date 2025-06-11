def top_purchased_products(df, filters):
    """
    Restituisce i prodotti più acquistati in base all'evento 'purchase'.
    """
    df_filtered = df.filter(df["EventType"] == "purchase")
    return df_filtered.groupBy("ProductID").count().orderBy("count", ascending=False)