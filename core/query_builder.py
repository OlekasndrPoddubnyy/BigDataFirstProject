# core/query_builder.py

import importlib
import json
import os
from config.settings import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def load_manifest():
    with open("manifest.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_dynamic_job(intent: dict) -> str:
    manifest = load_manifest()

    system_prompt = """Sei un esperto Spark. L'utente ti fornisce un intento semantico JSON e i dataset a disposizione. 
Il tuo compito è generare codice PySpark completo che produca un risultato chiamato `result`.
Non fornire spiegazioni. Rispondi solo con codice Python valido.
Il DataFrame Spark è già disponibile come variabile `spark`.
Il risultato deve essere assegnato a `result`, ad esempio: result = df.groupBy(...).agg(...)

Ogni dataset ha: nome, descrizione, colonne. Puoi usare join, filtri, aggregazioni, ecc.
"""

    user_prompt = {
        "intent": intent,
        "available_datasets": manifest["datasets"]
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt, indent=2)}
            ],
            temperature=0,
            max_tokens=1000
        )

        code = response.choices[0].message.content.strip()
        return code

    except Exception as e:
        return f"# Errore durante generazione job dinamico: {e}"

def build_static_job(intent: dict) -> str:
    """
    Costruisce un job Spark statico a partire dal dizionario dell'intento:
    {
        "domain": "hr",
        "intent": "turnover_per_department",
        "filters": {...}
    }

    Genera una stringa di codice Python eseguibile che assegna il risultato alla variabile `result`.
    """
    domain = intent.get("domain")
    action = intent.get("intent")
    filters = intent.get("filters", {})

    module_path = f"domain.{domain}.jobs"

    try:
        module = importlib.import_module(module_path)
        func = getattr(module, action)
        code = func(filters)
        return code

    except Exception as e:
        error_msg = (
            f"# Job statico non disponibile per {domain}.{action} → {e}"
        )
        return error_msg


