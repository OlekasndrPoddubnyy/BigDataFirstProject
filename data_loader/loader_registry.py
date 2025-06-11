import logging

from data_loader.loader_hr import load_hr
from data_loader.loader_sales import load_sales
from data_loader.loader_ecommerce import load_ecommerce

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Registrazione centralizzata
_LOADER_MAP = {
    "hr": load_hr,
    "sales": load_sales,
    "ecommerce": load_ecommerce,
}

def get_loader(name: str):
    """
    Ritorna la funzione loader per un nome dataset (es. "hr", "sales", "ecommerce").
    Lancia ValueError se il nome non è valido.
    """
    name = name.lower()
    if name in _LOADER_MAP:
        logger.debug(f"[loader_registry] Loader trovato per: {name}")
        return _LOADER_MAP[name]
    else:
        logger.error(f"[loader_registry] Loader non trovato per: {name}")
        raise ValueError(f"Loader non disponibile per '{name}'. Dataset supportati: {list(_LOADER_MAP.keys())}")
