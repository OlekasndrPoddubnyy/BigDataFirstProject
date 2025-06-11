import json
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_MANIFEST_PATH = os.path.join("manifest.json")

try:
    with open(_MANIFEST_PATH, "r", encoding="utf-8") as f:
        _manifest = json.load(f)
    logger.info("[JobContext] Manifest caricato correttamente.")
except Exception as e:
    logger.error(f"[JobContext] Errore caricamento manifest: {e}")
    _manifest = {"datasets": []}


def get_dataset_path(name: str) -> str:
    """
    Restituisce il path relativo al dataset specificato (es. "hr" → "data/hr.csv")
    """
    for ds in _manifest["datasets"]:
        if ds["name"].lower() == name.lower():
            return ds["path"]
    raise ValueError(f"Dataset '{name}' non trovato nel manifest.")


def get_dataset_columns(name: str) -> list[str]:
    """
    Restituisce la lista delle colonne di un dataset specificato.
    """
    for ds in _manifest["datasets"]:
        if ds["name"].lower() == name.lower():
            return ds["columns"]
    raise ValueError(f"Dataset '{name}' non trovato nel manifest.")


def describe_datasets() -> str:
    """
    Restituisce una descrizione in linguaggio naturale dei dataset disponibili,
    da passare come contesto al prompt LLM.
    """
    descrizioni = []
    for ds in _manifest["datasets"]:
        descrizioni.append(
            f"- {ds['name']}: {ds['description']} (Colonne: {', '.join(ds['columns'][:5])}...)"
        )
    return "I seguenti dataset sono disponibili:\n" + "\n".join(descrizioni)