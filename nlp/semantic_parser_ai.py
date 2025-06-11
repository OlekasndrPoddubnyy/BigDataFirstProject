import json
import re
import logging
from openai import OpenAI

from config.settings import OPENAI_API_KEY, TEST_APP, SPARK_LOG_LEVEL
from nlp.parser import fallback_parser

logger = logging.getLogger(__name__)
logger.setLevel(SPARK_LOG_LEVEL)

if not TEST_APP:
    client = OpenAI(api_key=OPENAI_API_KEY)


def semantic_parse_ai(text: str) -> dict:
    """
    Interpreta una frase in linguaggio naturale e restituisce
    un JSON strutturato con: dominio, intento, filtri.
    Usa OpenAI se disponibile, altrimenti fallback offline.
    """

    logger.info(f"[SemanticParser] Modalità: {'PROD (AI)' if TEST_APP else 'TEST (offline)'}")

    if TEST_APP:
        logger.warning("[SemanticParser] Nessuna API OpenAI trovata. Uso fallback parser.")
        return fallback_parser(text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"""Estrai dominio, intento e filtri da questa frase:

\"{text}\"

Rispondi **solo con JSON** in questo formato:

{{
  "domain": "...",
  "intent": "...",
  "filters": {{ }}
}}"""
                }
            ],
            temperature=0.2,
            max_tokens=800
        )

        content = response.choices[0].message.content.strip()
        logger.debug(f"[SemanticParser] Risposta LLM grezza:\n{content}")

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: estrazione manuale
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                return json.loads(match.group())
            else:
                raise ValueError("Risposta non contiene JSON valido.")

    except Exception as e:
        logger.error(f"[SemanticParser] Errore OpenAI: {e}")
        logger.info("[SemanticParser] Uso fallback parser.")
        return fallback_parser(text)