import logging
from openai import OpenAI

from config.settings import settings
from core.job_context import describe_datasets

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)

_USE_MOCK = not settings.use_openai

if not _USE_MOCK:
    client = OpenAI(api_key=settings.openai_api_key)


def generate_spark_job(intent_json: dict) -> str:
    """
    Dato un intent semantico, genera un job Spark (codice Python) da eseguire.
    """
    if _USE_MOCK:
        logger.warning("[JobPlannerAI] OPENAI non attivo. Uso fallback offline.")
        return mock_job(intent_json)

    try:
        prompt = build_prompt(intent_json)
        logger.debug(f"[JobPlannerAI] Prompt inviato:\n{prompt}")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": "Sei un esperto di Spark e big data. Rispondi solo con codice Python valido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )

        result = response.choices[0].message.content.strip()
        logger.debug("[JobPlannerAI] Codice ricevuto:")
        logger.debug(result)

        return result

    except Exception as e:
        logger.error(f"[JobPlannerAI] Errore OpenAI: {e}")
        return mock_job(intent_json)


def build_prompt(intent: dict) -> str:
    """
    Costruisce il prompt completo da inviare a OpenAI per generare job Spark.
    """
    intent_str = f"Intent: {intent['intent']}\nFiltri: {intent.get('filters', {})}"
    dataset_info = describe_datasets()

    return f"""
Scrivi un job Spark in Python che soddisfa la seguente richiesta dell'utente:

{intent_str}

Usa solo i dataset disponibili descritti qui sotto.
{dataset_info}

Restituisci solo il codice Python Spark, senza commenti o testo aggiuntivo.
"""


def mock_job(intent: dict) -> str:
    """
    Versione di fallback che genera codice fittizio utile per test.
    """
    if intent["domain"] == "hr":
        return """df = get_loader("hr")(spark)
df.groupBy("Department").count().orderBy("count", ascending=False).show()"""

    if intent["domain"] == "sales":
        return """dfs = get_loader("sales")(spark)
dfs["train"].groupBy("Store").sum("Sales").show()"""

    if intent["domain"] == "ecommerce":
        return """df = get_loader("ecommerce")(spark)
df.groupBy("ProductID").count().orderBy("count", ascending=False).show()"""

    return "# Nessun job disponibile per l'intent ricevuto."
