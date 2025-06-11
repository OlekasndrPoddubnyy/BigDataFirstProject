def turnover_per_department(df, filters):
    """
    Restituisce il numero di dipendenti per dipartimento,
    utile per analizzare il turnover.
    """
    return df.groupBy("Department").count().orderBy("count", ascending=False)