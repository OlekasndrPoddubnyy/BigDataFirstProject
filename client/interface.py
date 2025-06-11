# client/interface.py

def print_intro(is_test_mode: bool):
    print("\n Avvio DataWhiz Enterprise")
    if is_test_mode:
        print("Modalità TEST attiva: esecuzione automatica job statici\n")
    else:
        print("Benvenuto in DataWhiz Enterprise (modalità shell)")
        print("Scrivi la tua domanda oppure 'exit' per uscire.\n")

def prompt_test_questions():
    """
    Ritorna una lista di domande da eseguire in modalità test.
    Ogni domanda verrà interpretata e usata per testare il parser e i job statici.
    """
    return [
        "Mostrami il reparto con più turnover",
        "Mostrami le vendite del 2015 per ogni negozio",
        "Quali sono i prodotti più acquistati"
    ]